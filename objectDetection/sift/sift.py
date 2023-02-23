#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sift（Scale-invariant feature transform) (尺度不变特征变换)

b站教程视频:https://www.bilibili.com/video/BV1Qb411W7cK/?spm_id_from=333.337.search-card.all.click&vd_source=d3186b41f1a6229779fb4fe8e9ce0154
代码copy自这里:https://github.com/o0o0o0o0o0o0o/image-processing-from-scratch/blob/master/sift/SIFT.py
(这篇原理比较详细)原理、py代码:https://mp.weixin.qq.com/s?__biz=MzU0NjgzMDIxMQ==&mid=2247599504&idx=3&sn=b3e46e54abc43a2e8952a1d774f69897&chksm=fb54a77ccc232e6acd0af5be6f01a5133fa9bf8360658478dd5af7f5b14fcd98cc39f01660b3&scene=27
(这篇超详细)原理和C++代码详解:https://dezeming.top/wp-content/uploads/2021/07/Sift算法原理与OpenCV源码解读.pdf
"""

from PIL import Image
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import numpy as np
import cv2
import warnings
warnings.filterwarnings("ignore")  # 忽略警告


def convolve(filter, mat, padding, strides):
    result = None
    filter_size = filter.shape
    mat_size = mat.shape
    if len(filter_size) == 2:
        if len(mat_size) == 3:
            channel = []
            for i in range(mat_size[-1]):
                pad_mat = np.pad(
                    mat[:, :, i], ((padding[0], padding[1]), (padding[2], padding[3])), 'constant')
                temp = []
                for j in range(0, mat_size[0], strides[1]):
                    temp.append([])
                    for k in range(0, mat_size[1], strides[0]):
                        val = (
                            filter*pad_mat[j:j+filter_size[0], k:k+filter_size[1]]).sum()
                        temp[-1].append(val)
                channel.append(np.array(temp))

            channel = tuple(channel)
            result = np.dstack(channel)
        elif len(mat_size) == 2:
            channel = []
            pad_mat = np.pad(
                mat, ((padding[0], padding[1]), (padding[2], padding[3])), 'constant')
            for j in range(0, mat_size[0], strides[1]):
                channel.append([])
                for k in range(0, mat_size[1], strides[0]):
                    val = (
                        filter * pad_mat[j:j + filter_size[0], k:k + filter_size[1]]).sum()
                    channel[-1].append(val)

            result = np.array(channel)

    #print('convolve---result: ',result)
    return result


def downsample(img, step=2):
    return img[::step, ::step]


def GuassianKernel(sigma, dim):
    '''
    :param sigma: Standard deviation
    :param dim: dimension(must be positive and also an odd number)
    :return: return the required Gaussian kernel.
    '''
    temp = [t - (dim//2) for t in range(dim)]
    assistant = []
    for i in range(dim):
        assistant.append(temp)
    assistant = np.array(assistant)
    temp = 2*sigma*sigma
    result = (1.0/(temp*np.pi))*np.exp(-(assistant**2+(assistant.T)**2)/temp)
    
    #print('Guassian Kernel---result: ',result)
    return result

#计算高斯差分金字塔
def getDoG(img, n, sigma0, S=None, O=None):
    '''
    :param img: the original img.
    :param sigma0: sigma of the first stack of the first octave. default 1.52 for complicate reasons.
    :param n: how many stacks of feature that you wanna extract.一组里想提取多少层。
    :param S: how many stacks does every octave have. S must bigger than 3.
    :param k: the ratio of two adjacent stacks' scale.
    :param O: how many octaves do we have. 组数。(同样大小的图为一组)
    :return: the DoG Pyramid
    '''
    if S == None:
        S = n + 3 #3是因为S层高斯金字塔中只能提取S-1层高斯差分金字塔,而要找特征点就需要在竖直方向也能求导,所以最上层最下层也要去掉
    if O == None:
        O = int(np.log2(min(img.shape[0], img.shape[1]))) - 3 #这是原论文里推荐计算O值的公式

    k = 2 ** (1.0 / n)  
    sigma = [[(k**s)*sigma0*(1 << o) for s in range(S)] for o in range(O)]
    samplePyramid = [downsample(img, 1 << o) for o in range(O)]

    GuassianPyramid = []
    for i in range(O):
        GuassianPyramid.append([])
        for j in range(S):
            dim = int(6*sigma[i][j] + 1)
            if dim % 2 == 0:
                dim += 1
            GuassianPyramid[-1].append(convolve(GuassianKernel(
                sigma[i][j], dim), samplePyramid[i], [dim//2, dim//2, dim//2, dim//2], [1, 1]))
    DoG = [[GuassianPyramid[o][s+1] - GuassianPyramid[o][s]
            for s in range(S - 1)] for o in range(O)]

    #print('getDoG---DoG, GuassianPyramid: ',DoG, GuassianPyramid)
    return DoG, GuassianPyramid

#调整极值
'''
DoG:高斯差分金字塔。o,s:当前第几组、层。x, y: 当前像素坐标。
'''
def adjustLocalExtrema(DoG, o, s, x, y, contrastThreshold, edgeThreshold, sigma, n, SIFT_FIXPT_SCALE):
    SIFT_MAX_INTERP_STEPS = 5 #迭代次数超过5次，则判定为未找到准确特征点
    SIFT_IMG_BORDER = 5

    point = []

    #有限差分法求导。这里有说明:https://dezeming.top/wp-content/uploads/2021/07/Sift算法原理与OpenCV源码解读.pdf
    img_scale = 1.0 / (255 * SIFT_FIXPT_SCALE) #img_scale相当于对图像进行归一化，将DOG数据压缩到[ −1 ,1]之间
    deriv_scale = img_scale * 0.5 #一阶偏导系数(2h)
    second_deriv_scale = img_scale #二阶偏导系数(h^2)
    cross_deriv_scale = img_scale * 0.25 #二阶混合偏导系数(4h^2)

    img = DoG[o][s]
    i = 0
    while i < SIFT_MAX_INTERP_STEPS:
        if s < 1 or s > n or y < SIFT_IMG_BORDER or y >= img.shape[1] - SIFT_IMG_BORDER or x < SIFT_IMG_BORDER or x >= img.shape[0] - SIFT_IMG_BORDER:
            return None, None, None, None

        img = DoG[o][s]
        prev = DoG[o][s - 1]
        next = DoG[o][s + 1]
        
        dD = [(img[x, y + 1] - img[x, y - 1]) * deriv_scale, 
              (img[x + 1, y] - img[x - 1, y]) * deriv_scale,
              (next[x, y] - prev[x, y]) * deriv_scale]

        v2 = img[x, y] * 2
        dxx = (img[x, y + 1] + img[x, y - 1] - v2) * second_deriv_scale
        dyy = (img[x + 1, y] + img[x - 1, y] - v2) * second_deriv_scale
        dss = (next[x, y] + prev[x, y] - v2) * second_deriv_scale
        dxy = (img[x + 1, y + 1] - img[x + 1, y - 1] -
               img[x - 1, y + 1] + img[x - 1, y - 1]) * cross_deriv_scale
        dxs = (next[x, y + 1] - next[x, y - 1] -
               prev[x, y + 1] + prev[x, y - 1]) * cross_deriv_scale
        dys = (next[x + 1, y] - next[x - 1, y] -
               prev[x + 1, y] + prev[x - 1, y]) * cross_deriv_scale

        H = [[dxx, dxy, dxs], #海森矩阵。去除边缘效应
             [dxy, dyy, dys],
             [dxs, dys, dss]]

        X = np.matmul(np.linalg.pinv(np.array(H)), np.array(dD)) #np.matmul():矩阵乘法(matrix multiply)

        xi = -X[2]
        xr = -X[1]
        xc = -X[0]

        if np.abs(xi) < 0.5 and np.abs(xr) < 0.5 and np.abs(xc) < 0.5:
            break

        y += int(np.round(xc))
        x += int(np.round(xr))
        s += int(np.round(xi))

        i += 1

    if i >= SIFT_MAX_INTERP_STEPS:
        return None, x, y, s
    if s < 1 or s > n or y < SIFT_IMG_BORDER or y >= img.shape[1] - SIFT_IMG_BORDER or x < SIFT_IMG_BORDER or x >= \
            img.shape[0] - SIFT_IMG_BORDER:
        return None, None, None, None

    t = (np.array(dD)).dot(np.array([xc, xr, xi])) #.dot()矩阵乘法。
    #.matmul()和.dot()的区别：https://blog.csdn.net/Dontla/article/details/106498504
    #如果参与运算的是两个二维数组,官方更推荐使用np.matmul()和@用于矩阵乘法。https://www.cnblogs.com/ssyfj/p/12913015.html#%E4%B8%80%E7%82%B9%E7%A7%AFdot-product

    contr = img[x, y] * img_scale + t * 0.5 #舍去低对比度的点 :|fx| < T/n
    if np.abs(contr) * n < contrastThreshold:
        return None, x, y, s

    # 利用Hessian矩阵的迹和行列式计算主曲率的比值
    tr = dxx + dyy
    det = dxx * dyy - dxy * dxy
    if det <= 0 or tr * tr * edgeThreshold >= (edgeThreshold + 1) * (edgeThreshold + 1) * det:
        return None, x, y, s

    #保存特征点信息，因为不同的组会将图像降采样，所以关键点位置需要再乘以当前组数，得到在原图尺寸中的位置。
    point.append((x + xr) * (1 << o))
    point.append((y + xc) * (1 << o))
    #按格式保存特征点所在的组、层以及插值后的层的偏移量
    point.append(o + (s << 8) + (int(np.round((xi + 0.5)) * 255) << 16))
    #特征点相对于输入图像的尺度。因为我们设置的输入图像是实际输入图像扩大一倍以后的图像，因此要乘以2
    point.append(sigma * np.power(2.0, (s + xi) / n)*(1 << o) * 2)

    #print('adjust LocalExtrema---point, x, y, s: ',point, x, y, s)
    return point, x, y, s


#得到主方向
def GetMainDirection(img, r, c, radius, sigma, BinNum):
    expf_scale = -1.0 / (2.0 * sigma * sigma)

    X = []
    Y = []
    W = []
    temphist = []

    for i in range(BinNum):
        temphist.append(0.0)

    # 图像梯度直方图统计的像素范围
    k = 0
    for i in range(-radius, radius+1):
        y = r + i
        if y <= 0 or y >= img.shape[0] - 1:
            continue
        for j in range(-radius, radius+1):
            x = c + j
            if x <= 0 or x >= img.shape[1] - 1:
                continue

            dx = (img[y, x + 1] - img[y, x - 1])
            dy = (img[y - 1, x] - img[y + 1, x])

            X.append(dx)
            Y.append(dy)
            W.append((i * i + j * j) * expf_scale)
            k += 1

    length = k

    W = np.exp(np.array(W)) #高斯权重
    Y = np.array(Y)
    X = np.array(X)
    Ori = np.arctan2(Y, X)*180/np.pi #梯度方向
    Mag = (X**2+Y**2)**0.5 #梯度幅值

    # 计算直方图的每个bin
    for k in range(length):
        bin = int(np.round((BinNum / 360.0) * Ori[k]))
        if bin >= BinNum:
            bin -= BinNum
        if bin < 0:
            bin += BinNum
        temphist[bin] += W[k] * Mag[k]

    # smooth the histogram
    # 高斯平滑
    temp = [temphist[BinNum - 1], temphist[BinNum - 2], temphist[0], temphist[1]]
    temphist.insert(0, temp[0])
    temphist.insert(0, temp[1])
    temphist.insert(len(temphist), temp[2])
    temphist.insert(len(temphist), temp[3])      # padding

    hist = []
    for i in range(BinNum):
        hist.append((temphist[i] + temphist[i+4]) * (1.0 / 16.0) + (
            temphist[i+1] + temphist[i+3]) * (4.0 / 16.0) + temphist[i+2] * (6.0 / 16.0))

    # 得到主方向
    maxval = max(hist)

    #print('Get Main Direction---maxval: ',maxval, 'Get Main Direction---hist: ',hist)
    return maxval, hist

#找极值(关键点)
'''
contrastThreshold 用来过滤掉太小的点(噪声)
edgeThreshold 过滤掉边缘
'''
def LocateKeyPoint(DoG, sigma, GuassianPyramid, n, BinNum=36, contrastThreshold=0.04, edgeThreshold=10.0):
    SIFT_ORI_SIG_FCTR = 1.52
    SIFT_ORI_RADIUS = 3 * SIFT_ORI_SIG_FCTR
    SIFT_ORI_PEAK_RATIO = 0.8

    SIFT_INT_DESCR_FCTR = 512.0
    # SIFT_FIXPT_SCALE = 48
    SIFT_FIXPT_SCALE = 1 #*？SIFT_FIXPT_SCALE是什么

    KeyPoints = []
    O = len(DoG)
    S = len(DoG[0])
    for o in range(O): #高斯差分金字塔中每一组
        for s in range(1, S-1): #每一组里的每一层
            threshold = 0.5*contrastThreshold/(n*255*SIFT_FIXPT_SCALE)
            img_prev = DoG[o][s-1] #对比上一层、下一层
            img = DoG[o][s]
            img_next = DoG[o][s+1]
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    val = img[i, j] 
                    #在立体八邻域找极值(都叫eight但上、下层中是9个像素)
                    #这里的max、min是为了不超出图片范围。-1、+2是因为左闭右开[)。
                    eight_neiborhood_prev = img_prev[max(0, i - 1):min(i + 2, img_prev.shape[0]), 
                                                     max(0, j - 1):min(j + 2, img_prev.shape[1])]
                    eight_neiborhood = img[max(0, i - 1):min(i + 2, img.shape[0]), 
                                           max(0, j - 1):min(j + 2, img.shape[1])]
                    eight_neiborhood_next = img_next[max(0, i - 1):min(i + 2, img_next.shape[0]), 
                                                     max(0, j - 1):min(j + 2, img_next.shape[1])]
                    #if值大于阈值、且>0并大于所有领域中的值、或者<0并小于所有领域中的值
                    if np.abs(val) > threshold and \
                        ((val > 0 and (val >= eight_neiborhood_prev).all() and (val >= eight_neiborhood).all() and (val >= eight_neiborhood_next).all())
                         or (val < 0 and (val <= eight_neiborhood_prev).all() and (val <= eight_neiborhood).all() and (val <= eight_neiborhood_next).all())):

                        point, x, y, layer = adjustLocalExtrema(
                            DoG, o, s, i, j, contrastThreshold, edgeThreshold, sigma, n, SIFT_FIXPT_SCALE)
                        if point == None:
                            continue

                        scl_octv = point[-1]*0.5/(1 << o)
                        omax, hist = GetMainDirection(GuassianPyramid[o][layer], x, y, int(
                            np.round(SIFT_ORI_RADIUS * scl_octv)), SIFT_ORI_SIG_FCTR * scl_octv, BinNum)
                        mag_thr = omax * SIFT_ORI_PEAK_RATIO
                        for k in range(BinNum):
                            if k > 0:
                                l = k - 1
                            else:
                                l = BinNum - 1
                            if k < BinNum - 1:
                                r2 = k + 1
                            else:
                                r2 = 0
                            if hist[k] > hist[l] and hist[k] > hist[r2] and hist[k] >= mag_thr:
                                bin = k + 0.5 * \
                                    (hist[l]-hist[r2]) / \
                                    (hist[l] - 2 * hist[k] + hist[r2])
                                if bin < 0:
                                    bin = BinNum + bin
                                else:
                                    if bin >= BinNum:
                                        bin = bin - BinNum
                                temp = point[:]
                                temp.append((360.0/BinNum) * bin)
                                KeyPoints.append(temp)
                                
    #print('Locate KeyPoint---KeyPoints: ',KeyPoints)
    return KeyPoints

#计算描述符
def calcSIFTDescriptor(img, ptf, ori, scl, d, n, SIFT_DESCR_SCL_FCTR=3.0, SIFT_DESCR_MAG_THR=0.2, SIFT_INT_DESCR_FCTR=512.0, FLT_EPSILON=1.19209290E-07):
    dst = []
    pt = [int(np.round(ptf[0])), int(np.round(ptf[1]))]  # 坐标点取整
    cos_t = np.cos(ori * (np.pi / 180))  # 余弦值
    sin_t = np.sin(ori * (np.pi / 180))  # 正弦值
    bins_per_rad = n / 360.0
    exp_scale = -1.0 / (d * d * 0.5)
    hist_width = SIFT_DESCR_SCL_FCTR * scl
    radius = int(np.round(hist_width * 1.4142135623730951 * (d + 1) * 0.5))
    cos_t /= hist_width
    sin_t /= hist_width

    rows = img.shape[0]
    cols = img.shape[1]

    hist = [0.0]*((d+2)*(d+2)*(n+2))
    X = []
    Y = []
    RBin = []
    CBin = []
    W = []

    k = 0
    for i in range(-radius, radius+1):
        for j in range(-radius, radius+1):

            c_rot = j * cos_t - i * sin_t
            r_rot = j * sin_t + i * cos_t
            rbin = r_rot + d // 2 - 0.5   # //：向下取整的除法
            cbin = c_rot + d // 2 - 0.5
            r = pt[1] + i
            c = pt[0] + j

            if rbin > -1 and rbin < d and cbin > -1 and cbin < d and r > 0 and r < rows - 1 and c > 0 and c < cols - 1:
                dx = (img[r, c+1] - img[r, c-1])
                dy = (img[r-1, c] - img[r+1, c])
                X.append(dx)
                Y.append(dy)
                RBin.append(rbin)
                CBin.append(cbin)
                W.append((c_rot * c_rot + r_rot * r_rot) * exp_scale)
                k += 1

    length = k
    Y = np.array(Y)
    X = np.array(X)
    Ori = np.arctan2(Y, X)*180/np.pi
    Mag = (X ** 2 + Y ** 2) ** 0.5
    W = np.exp(np.array(W))

    for k in range(length):
        rbin = RBin[k] #得到d*d邻域区域的坐标,即三维直方图的底内的位置
        cbin = CBin[k]
        obin = (Ori[k] - ori) * bins_per_rad #得到幅角的所属的8个等分中的一个,即直方图的高度。bins_per_rad =n/360
        mag = Mag[k] * W[k] #得到高斯加权以后的梯度幅值

        #r0 c0 o0 为三维坐标的整数部分，表示属于那个正方体，因为正方体个数是固定的，且为整数
        r0 = int(rbin)
        c0 = int(cbin)
        o0 = int(obin)
        #rbin cbin obin 为三维坐标的小数部分，也就是上图中小正方体c的坐标
        rbin -= r0
        cbin -= c0
        obin -= o0


        if o0 < 0: #把角度调整到0~360°之间
            o0 += n
        if o0 >= n:
            o0 -= n

        # histogram update using tri-linear interpolation。三线性插值
        v_r1 = mag * rbin
        v_r0 = mag - v_r1

        v_rc11 = v_r1 * cbin
        v_rc10 = v_r1 - v_rc11

        v_rc01 = v_r0 * cbin
        v_rc00 = v_r0 - v_rc01

        v_rco111 = v_rc11 * obin
        v_rco110 = v_rc11 - v_rco111

        v_rco101 = v_rc10 * obin
        v_rco100 = v_rc10 - v_rco101

        v_rco011 = v_rc01 * obin
        v_rco010 = v_rc01 - v_rco011

        v_rco001 = v_rc00 * obin
        v_rco000 = v_rc00 - v_rco001
        
        #得到该像素点在三维直方图中的索引
        idx = ((r0 + 1) * (d + 2) + c0 + 1) * (n + 2) + o0 
        #8个顶点对应于坐标平移前的8个直方图正方体，对其进行累加求和
        hist[idx] += v_rco000
        hist[idx+1] += v_rco001
        hist[idx + (n+2)] += v_rco010
        hist[idx + (n+3)] += v_rco011
        hist[idx+(d+2) * (n+2)] += v_rco100
        hist[idx+(d+2) * (n+2)+1] += v_rco101
        hist[idx+(d+3) * (n+2)] += v_rco110
        hist[idx+(d+3) * (n+2)+1] += v_rco111

    # finalize histogram, since the orientation histograms are circular
    # 角度是循环的, 所以要给最终的描述符加上循环部分的hist 
    for i in range(d):
        for j in range(d):
            idx = ((i+1) * (d+2) + (j+1)) * (n+2)
            hist[idx] += hist[idx+n]
            hist[idx+1] += hist[idx+n+1]
            for k in range(n):
                dst.append(hist[idx+k])

    #copy histogram to the descriptor,apply hysteresis thresholding　and scale the result, so that it can be easily converted　to byte array
    nrm2 = 0
    length = d * d * n
    for k in range(length):
        nrm2 += dst[k] * dst[k]
    thr = np.sqrt(nrm2) * SIFT_DESCR_MAG_THR #对光照阈值进行反归一化处理, SIFT_DESCR_MAG_THR=0.2

    nrm2 = 0
    for i in range(length):
        val = min(dst[i], thr) #把特征矢量中大于反归一化阈值的元素用thr 替代
        dst[i] = val
        nrm2 += val * val
    nrm2 = SIFT_INT_DESCR_FCTR / max(np.sqrt(nrm2), FLT_EPSILON)
    for k in range(length):
        dst[k] = min(max(dst[k] * nrm2, 0), 255)

    #print('calc SIFTDescriptor---dst: ',dst)
    return dst

#构建关键点的描述符
def calcDescriptors(gpyr, keypoints, SIFT_DESCR_WIDTH=4, SIFT_DESCR_HIST_BINS=8):
    # SIFT_DESCR_WIDTH = 4，描述直方图的宽度
    # SIFT_DESCR_HIST_BINS = 8
    d = SIFT_DESCR_WIDTH
    n = SIFT_DESCR_HIST_BINS
    descriptors = []

    for i in range(len(keypoints)):
        kpt = keypoints[i]
        o = kpt[2] & 255
        s = (kpt[2] >> 8) & 255  # 该特征点所在的组序号和层序号
        scale = 1.0 / (1 << o)  # 缩放倍数
        size = kpt[3] * scale  # 该特征点所在组的图像尺寸
        ptf = [kpt[1] * scale, kpt[0] * scale]  # 该特征点在金字塔组中的坐标
        img = gpyr[o][s]  # 该点所在的金字塔图像

        descriptors.append(calcSIFTDescriptor(
            img, ptf, kpt[-1], size * 0.5, d, n))
        
    #print('calcDescriptors---descriptors: ',descriptors)
    return descriptors


def do_sift(img, showDoGimgs=False):
    SIFT_SIGMA = 1.6  #希望第一次卷积后能达到的尺度
    SIFT_INIT_SIGMA = 0.5  # 假设的摄像头的尺度(即假设的原图自带的模糊尺度)
    sigma0 = np.sqrt(SIFT_SIGMA**2-SIFT_INIT_SIGMA**2)
    n = 3

    DoG, GuassianPyramid = getDoG(img, n, sigma0)
    if showDoGimgs:
        for i in DoG:
            for j in i:
                plt.imshow(j.astype(np.uint8), cmap='gray')
                plt.axis('off')
                plt.show()

    KeyPoints = LocateKeyPoint(DoG, SIFT_SIGMA, GuassianPyramid, n)
    discriptors = calcDescriptors(GuassianPyramid, KeyPoints)

    #print('do_sift---KeyPoints, discriptors: ',KeyPoints, discriptors)
    return KeyPoints, discriptors

#画线
def drawLines(img, info, color=(255, 0, 0), err=700):
    if len(img.shape) == 2:
        result = np.dstack((img, img, img))
    else:
        result = img
    k = 0
    #print('draw Lines---info[:, 1],info[:, 0]:',info[:, 1],info[:, 0])
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            temp = (info[:, 1]-info[:, 0])
            A = (j - info[:, 0])*(info[:, 3]-info[:, 2])
            B = (i - info[:, 2])*(info[:, 1]-info[:, 0])
            temp[temp == 0] = 1e-9
            t = (j-info[:, 0])/temp
            e = np.abs(A-B)
            temp = e < err
            if (temp*(t >= 0)*(t <= 1)).any():
                result[i, j] = color
                k += 1
    #print('Lines---k',k)

    return result

#连接两张图的特征点
'''
num: 连多少组特征点
'''
def drawKeyPointsLines(X1, X2, Y1, Y2, dis, img, num=10):
    #plt.clf()
  
    info = list(np.dstack((X1, X2, Y1, Y2, dis))[0])
    info = sorted(info, key=lambda x: x[-1])
    info = np.array(info)
    #print('draw KeyPointsLines---len(info): ',len(info))
    info = info[:min(num, info.shape[0]), :]
    #print('draw KeyPointsLines---len(info-2): ',len(info))
    #print('draw KeyPointsLines---info-2: ',info)
    img = drawLines(img, info)
    plt.imsave('./imgs/output_1.jpg', img)

    if len(img.shape) == 2:
        plt.imshow(img.astype(np.uint8), cmap='gray')
    else:
        plt.imshow(img.astype(np.uint8))
    plt.axis('off')
    '''plt.plot([info[:,0], info[:,1]], [info[:,2], info[:,3]], 'c')
    fig = plt.gcf()
    fig.set_size_inches(int(img.shape[0]/100.0),int(img.shape[1]/100.0))
    plt.savefig('./imgs/output_2.jpg')'''
    plt.show()

#圈出特征点和主方向
def drawKeyPoints(img,KeyPoints):
  plt.imshow(img)
  for keyPiont in KeyPoints:
    #print('keyPiont',keyPiont)
    #画空心圆的方法: facecolors='none', edgecolors='r'
    plt.scatter(keyPiont[0], keyPiont[1], facecolors='none', edgecolors='r', s=200)
  plt.show()

if __name__ == '__main__':
    origimg = plt.imread('./imgs/cat_1_medium.jpeg')
    #plt.imshow(origimg)
    if len(origimg.shape) == 3:
        img = origimg.mean(axis=-1)#如果是彩图,用.mean()给图像去均值
    else:
        img = origimg
    keyPoints, discriptors = do_sift(img)

    origimg2 = plt.imread('./imgs/cat_2_medium.jpeg')
    #plt.imshow(origimg2)
    if len(origimg.shape) == 3:
        img2 = origimg2.mean(axis=-1)
    else:
        img2 = origimg2
    ScaleRatio = img.shape[0]*1.0/img2.shape[0]#.shape[0]图片高度

    img2 = np.array(Image.fromarray(img2).resize(
        (int(round(ScaleRatio * img2.shape[1])), img.shape[0]), Image.BICUBIC))
    keyPoints2, discriptors2 = do_sift(img2, True)

    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(discriptors, [0]*len(discriptors))
    match = knn.kneighbors(discriptors2, n_neighbors=1, return_distance=True)

    keyPoints = np.array(keyPoints)[:, :2]
    keyPoints2 = np.array(keyPoints2)[:, :2]
    #print('keyPoints',keyPoints,'keyPoints2',keyPoints2)
    #drawKeyPoints(origimg,keyPoints)

    keyPoints2[:, 1] = img.shape[1] + keyPoints2[:, 1]

    origimg2 = np.array(Image.fromarray(origimg2).resize(
        (img2.shape[1], img2.shape[0]), Image.BICUBIC))
    result = np.hstack((origimg, origimg2))

    keyPoints = keyPoints[match[1][:, 0]]
    drawKeyPoints(origimg,keyPoints)

    X1 = keyPoints[:, 1]
    X2 = keyPoints2[:, 1]
    Y1 = keyPoints[:, 0]
    Y2 = keyPoints2[:, 0]
    

    drawKeyPointsLines(X1, X2, Y1, Y2, match[0][:, 0], result,15)
    
    #直接用opencv的sift
    '''
    img = cv2.imread('./imgs/cat_2_medium.jpeg')
    # convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    # find the keypoints on image (grayscale)
    kp = sift.detect(gray,None)
    img_ky=cv2.drawKeypoints(gray,kp,None,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)    
    # display the image with keypoints drawn on it
    cv2.imshow("Keypoints", img_ky)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
