%%
%% Sammenlimt av Håvard Berland <http://www.math.ntnu.no/~berland/>
%% Etter sammenliming, flikket på av Harald Hanche-Olsen.
%% 
%%  Nesten all kode limt inn fra NTNUeksamen.cls 
%%  og imftechnote.cls av Harald Hanche-Olsen.


%% Identification part
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{NTNUoving}[2004/10/15 Klassefil for ovinger ved NTNU]

%% Declaration of options

\newtoks\langinfo\langinfo{}
\DeclareOption{langinfo}{\langinfo{\LANGINFO}}

\DeclareOption{graalogo}{\def\logofil{ntnulogosort}}% NTNU-policy
\DeclareOption{sortlogo}{\def\logofil{ntnulogosort}}
\DeclareOption{twoclumn}{\OptionNotUsed}
\newif\ifgeometry\geometrytrue
\DeclareOption{nogeometry}{\geometryfalse}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}

\def\logofil{ntnulogoblaa} % Default er å bruke blå logo.

%% Execution of options
\ProcessOptions\relax

%% Package loading
\LoadClass{article} % Father class.
\RequirePackage{babel}
\RequirePackage{graphicx}
\RequirePackage{amssymb}
\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{lastpage}
\ifgeometry
  \RequirePackage[margin=3cm]{geometry}
\fi

%% Main code




%%% Fix a bug in babel's addto:
%%% Stuffing text in a token register doubles any # therein (?)
%%% so if the second arg contained any #, is was handled differently
%%% depending on whether #1 was defined or not.
\def\addto#1#2{{\ifx#1\undefined\toks@{#2}\else\toks@\expandafter{#1#2}\fi
                \xdef#1{\the\toks@}}}
\addto\extrasnorsk{%
  \def\PageText#1#2{Side #1 av #2}%
  \def\NTNUa{Norges teknisk--naturvitenskapelige universitet}%
  \def\NTNUi{Sett meg med \textbackslash institutt-kommandoen}%
  \def\OVING{Innlevering}%
  \def\LANGINFO{Bokm{\aa}l}%
}
\addto\extrasnynorsk{%
  \def\PageText#1#2{Side #1 av #2}%
  \def\NTNUa{Noregs teknisk--naturvitskaplege universitet}%
  \def\NTNUi{Set meg med \textbackslash institutt-kommandoen}%
  \def\OVING{Innlevering}%
  \def\LANGINFO{Nynorsk}%
}
\addto\extrasenglish{%
  \def\PageText#1#2{Page #1 of #2}%
  \def\NTNUa{Norwegian University of Science and Technology}%
  \def\NTNUi{Set me with the \textbackslash institutt-command}%
  \def\OVING{Exercise set}
  \def\LANGINFO{English}%
}

% Convenience commands. Setter alle tre språk.
\newcommand{\institutt}[1]{%
  \addto{\extrasnorsk}{\def\NTNUi{#1}}%
  \addto{\extrasnynorsk}{\def\NTNUi{#1}}%
  \addto{\extrasenglish}{\def\NTNUi{#1}}%
}
\newcommand{\ovingstekst}[1]{%
  \addto{\extrasnorsk}{\def\OVING{#1}}%
  \addto{\extrasnynorsk}{\def\OVING{#1}}%
  \addto{\extrasenglish}{\def\OVING{#1}}%
}

\newcommand{\oppgaveoverskrift}[1]{\textbf{#1}\par}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Bruk:
%
% \documentclass[12pt,a4paper, norsk]{NTNUoving}
% 
% \fag{TMA4100 Matematikk 1}
% \ovingnr{1}
% \semester{Vår 2005}
% \institutt{Institutt for matematiske fag}
%
% %% Valgfri alternativ tekst for 'Ã˜ving':
% %% \ovingstekst{Oppgavesett}
%
% \begin{document}
%
% \begin{oppgave}
%   <introtekst>
%
%   \begin{punkt}
%     <oppgavetekst>
%   \end{punkt}
%
%   \begin{punkt}
%     <oppgavetekst>
%   \end{punkt}
% 
% \end{oppgave}
%
% \end{document}

%%%%%%%%%%%%%%%%


\AtBeginDocument{\maketitle}

\setlength{\parindent}{0pt}
\setlength{\parskip}{12pt plus 6pt}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Oppgaver
\newcounter{Oppg}
\newenvironment{oppgave}[1][\theOppg]%
{  \refstepcounter{Oppg}
  \list{}{\setlength{\topsep}{\baselineskip}}
  \item[{\fbox{\sffamily\large {#1}}}]}
  {\endlist}

%%% Punkter i hver oppgave
\newcounter{Punkt}[Oppg]
\renewcommand{\thePunkt}{\alph{Punkt}}
\newcommand{\Punktkolon}{)}
\newcommand{\PunktInn}{2em}
\newenvironment{punkt}%
 {\refstepcounter{Punkt}%
  \list{}{\setlength{\topsep}{0pt}}
  \item[{\bf \thePunkt\Punktkolon}]}
 {\endlist}



\def\maketitle{\par
 \begingroup
   \def\thefootnote{\fnsymbol{footnote}}
   \def\@makefnmark{\hbox   
       to 0pt{$^{\@thefnmark}$\hss}}   
   \newpage
    \global\@topnum\z@        % Prevents figures from going at top of page.
    \@maketitle 
 \endgroup
 \setcounter{footnote}{0}
 \let\maketitle\relax
 \let\@maketitle\relax
 \thispagestyle{titlepage}}



%% Denne makroen tegner linjene og boksen rundt tittelen.
\def\@maketitle{\newpage
  \null
  \vskip -40pt % \headheight + \headsep
  \hrule height 0.4pt \nointerlineskip
  \vskip 1.2pt
  \hrule height 2.0pt \nointerlineskip
  \hbox{\vrule width 0.4pt
   \begingroup\advance\hsize by -0.8pt\vbox{\@m@ketitle}\endgroup
   \vrule width 0.4pt} \nointerlineskip
  \hrule height 2.0pt \nointerlineskip
  \vskip 1.2pt
  \hrule height 0.4pt \nointerlineskip
 \vskip 25pt
}

\def\@m@ketitle{
  \vskip 2mm 
  \hbox to\textwidth{\kern4mm
    \vtop{\null\hbox{\NTNULogo}}\hfill
    \vtop{\null\hbox{\parbox{0.4\textwidth}{
      \LARGE \raggedleft \@title \par
      \@ifundefined{@ving}
      {}
      {\vskip 1em
       \large\textbf{\@ving}}}}}%
    \kern4mm}
  \vskip 0.5em}

% Forsiden har en spesiell ``page style'' {\tt titlepage} som er tom
% {\o}verst men lik den vanlige nederst.
\def\ps@titlepage{%
  \let\@mkboth\@gobbletwo
  \def\@oddhead{}\let\@evenhead\@oddhead
  \def\@oddfoot{\@techfoot}\let\@evenfoot\@oddfoot
  \def\sectionmark##1{}\def\subsectionmark##1{}}

\def\ps@tech{%
  \let\@mkboth\@gobbletwo
  \def\@oddhead{\@techhead}\let\@evenhead\@oddhead
  \def\@oddfoot{\@techfoot}\let\@evenfoot\@oddfoot
  \def\sectionmark##1{}\def\subsectionmark##1{}}

\def\@techfoot{%
\vbox{
  \hrule height 0.4pt\nointerlineskip
  \vskip 1.2pt
  \hrule height 2.0pt
  \vskip 2.0pt
  \hbox to \textwidth{\hbox to 0pt{\innerfoot\hss}%
    \hfil\centerfoot\hfil\hbox to 0pt{\hss\outerfoot}}}}

\def\@techhead{%
\vbox{
  \hbox to \textwidth{\hbox to 0pt{\innerhead\hss}%
    \hfil\centerhead\hfil\hbox to 0pt{\hss\outerhead}}\nointerlineskip
  \vskip 2.0pt
  \hrule height 2.0pt\nointerlineskip
  \vskip 1.2pt
  \hrule height 0.4pt
}}

\ps@tech
\headheight18pt
\headsep22pt

\let\@version\relax
\def\version#1{\def\@version{#1}}
\def\innerfoot{\the\langinfo}
%\def\innerfoot{\jobname\ifx\@version\relax\else\ versjon \@version\fi}
\def\centerfoot{\today}
\def\outerfoot{\PageText{\thepage}{\pageref{LastPage}}}
\def\innerhead{}
\def\centerhead{}
\def\outerhead{\@ving}


\newcommand{\NTNULogo}{
  %%  \hspace{-\parindent}
  \parbox[b]{0.4\textwidth}{
%    \rule{0mm}{2mm}\\ % instead of \vspace
    \includegraphics[width=2cm]{\logofil} \\
    \raggedright \NTNUa \\
    \NTNUi   }
}
\newcommand{\semester}[1]{\newcommand{\thesemester}{#1}}
\newcommand{\fag}[1]{\title{#1 \\  \thesemester}}
\newcommand{\oving}[1]{\gdef\@ving{#1}}
\newcommand{\ovingnr}[1]{\oving{\OVING\space#1}}
\renewcommand{\author}[1]{%
  \errhelp{There is no place to put an author name in this kind of document.}%
  \errmessage{\string\author\space is not supported (ignored)}}
\renewcommand{\thanks}[1]{%
  \errhelp{Making exercises for students earns you no thanks.}%
  \errmessage{\string\thanks\space is not supported (ignored)}}