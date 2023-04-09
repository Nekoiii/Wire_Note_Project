\version "2.24.1"
% automatically converted by musicxml2ly from /Users/nekosa/code/WireNote/music_processing/output_sheets/output.musicxml
\pointAndClickOff

\header {
    encodingsoftware =  "music21 v.7.3.3"
    encodingdate =  "2023-04-09"
    }

#(set-global-staff-size 20.0)
\paper {
    
    }
\layout {
    \context { \Score
        autoBeaming = ##f
        }

    }
PartPcdThreeThreefaFiveThreeOnedThreeTwocSixcOnebbOneTwoZeroFiveNineThreeFourThreeTwoeFoureSeveneVoiceOne = 
\relative c' {
    \clef "treble" \numericTimeSignature\time 4/4 | % 1
    c4 \bar "|."
    }


% The score definition
\score {
    <<
        
        \new Staff
        <<
            
            \context Staff << 
                \mergeDifferentlyDottedOn\mergeDifferentlyHeadedOn
                \context Voice = "PartPcdThreeThreefaFiveThreeOnedThreeTwocSixcOnebbOneTwoZeroFiveNineThreeFourThreeTwoeFoureSeveneVoiceOne" {  \PartPcdThreeThreefaFiveThreeOnedThreeTwocSixcOnebbOneTwoZeroFiveNineThreeFourThreeTwoeFoureSeveneVoiceOne }
                >>
            >>
        
        >>
    \layout {
  \context {
    \Staff
    \remove "Staff_symbol_engraver"
  }}
    % To create MIDI output, uncomment the following line:
    %  \midi {\tempo 4 = 100 }
    }

