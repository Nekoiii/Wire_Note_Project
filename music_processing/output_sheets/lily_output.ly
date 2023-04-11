
\version "2.24.1"

\paper {
  % 设置底色为grey
  bgcolor = #grey
}

\score {
  \new Staff {

\fixed c'{
c d e f
c' d e f
cis dis eis fis
}

}

\layout {
\hide Staff.StaffSymbol 
%\override NoteHead.color = #white
%\override Staff.Clef.color = #white
%Staff.BarLine=#white
}

}
