%\NeedsTeXFormat{LaTeX2e}[1999/12/01]
\ProvidesClass{labreport}

%% This document class is based on the standard 'article' class.
%% The only allowed options concern the choice of language.
%% The default language is USenglish.
\def \labreport@language {USenglish}
\DeclareOption{american}{\def \labreport@language {USenglish}}
\DeclareOption{english}{\def \labreport@language {UKenglish}}
\DeclareOption{UKenglish}{\def \labreport@language {UKenglish}}
\DeclareOption{USenglish}{\def \labreport@language {USenglish}}
\DeclareOption*{\ClassWarningNoLine{labreport}{Class option \CurrentOption
    \space is illegal in this document class}}
\ProcessOptions \relax
\LoadClass{article}

%% Select language.
\RequirePackage[\labreport@language]{babel}

%% Additional user interface:
\newcommand{\affiliation}[1]{\footnote{#1}}
\newcommand{\labreportdoi}[1]{\def \labreport@doi {#1}}
  \def \labreport@doi {some-doi}
\newcommand{\labreportfirstpage}[1]{\def \labreport@firstpage {#1}}
  \def \labreport@firstpage {1}
\newcommand{\labreportpublished}[1]{\def \labreport@publ {#1}}
  \def \labreport@publ {dd mmm yyyy}
\newcommand{\labreportreceived}[1]{\def \labreport@rec {#1}}
  \def \labreport@rec {dd mmm yyyy}
\newcommand{\labreportvolume}[1]{\def \labreport@vol {#1}}
  \def \labreport@vol {??}
\newcommand{\labreportyear}[1]{\def \labreport@year {#1}}
  \def \labreport@year {\the\year}
\newcommand{\keywords}[1]{\paragraph*{Keywords:}~~#1}
\newcommand{\shortauthor}[1]{\def \labreport@shortauthor {#1}}
  \def \labreport@shortauthor {Author's name}
\newcommand{\shorttitle}[1]{\def \labreport@shorttitle {#1}}
  \def \labreport@shorttitle {Title}
\newcommand{\course}[1]{\def \labreport@course {#1}}
  \def \labreport@course {Course}
%% The graphicx package is needed for the header image.
\RequirePackage{graphicx}
\RequirePackage{tikz}

%% Allow for math notation
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsfonts}
\RequirePackage{siunitx}
\sisetup{separate-uncertainty=true}
\sisetup{range-phrase=-}
\sisetup{range-units=single}
\RequirePackage[version=4]{mhchem}
\RequirePackage{gensymb}
\let\arrowvec\Vec
\renewcommand{\Vec}[1]{\mathbf{#1}}

% Bold figure labels
\RequirePackage{caption}
% \RequirePackage{subcaption}
\captionsetup{labelfont=bf}
\captionsetup{font=footnotesize}
\captionsetup{margin=0.3cm}

%% Headers should be in a steel blue colour.
\RequirePackage{color}
\definecolor{labreport@blue}{RGB}{37,40,45}

%% Select a suitable font:
%% The recommendation is Calibri 10 pt, but Computer Modern Bright
%% looks quite similar.
\RequirePackage[enlarged-baselineskips]{cmbright}
\RequirePackage[T1]{fontenc}
\pretolerance = 2000
\tolerance = 3000   \hbadness = \tolerance

%% Specify text dimensions and margins:
\RequirePackage[a4paper,margin=1.5cm,includefoot,top=2.5cm]{geometry}
\setlength{\columnsep}{1cm}

%% Define the headers and footers:
\RequirePackage{fancyhdr}
\RequirePackage{textcomp}
\setlength{\headheight}{12.5pt}
\fancyhead[C]{\color{labreport@blue}\small\sl 
  \labreport@shortauthor: 
  \labreport@shorttitle
  %. NMI, 
  %\labreport@vol, 
  %\labreport@firstpage--\lastpageref{VeryLastPage}
  %, \labreport@year
  }
\fancyhead[L,R]{}
\renewcommand{\headrulewidth}{0pt}
\setlength{\footskip}{40pt}
\fancyfoot[C]{\arabic{page}}
\fancyfoot[L,R]{}
\pagestyle{fancy}

% Do stuff with tables
\RequirePackage{booktabs}
\RequirePackage{makecell}
\RequirePackage{tabularx}
% \newcommand{\oldtoprule}{\toprule}
% \renewcommand{\toprule}{\vspace{3pt} \oldtoprule}

%% The front page:
\RequirePackage{transparent}

\fancypagestyle{plain}{%
  \fancyhead[C]{\makebox[\headwidth]{\raisebox{-2cm}[0pt][0pt]{%
      \transparent{1.0}
      \includegraphics[width=\textwidth]{header.jpg}}}}%
  \fancyhead[L,R]{}%
  \renewcommand{\headrulewidth}{0pt}%
  \fancyfoot[C,R]{}%
  \fancyfoot[L]{\raisebox{10pt}{\begin{minipage}{\textwidth}\raggedright
        \color{labreport@blue}\footnotesize 
        % \textcopyright~\labreport@year~Author(s).
        % This is an open access article licensed under the
        % Creative Commons Attribution License~4.0. 
        % (\url{http://creativecommons.org/licenses/by/4.0/}).
      \end{minipage}}}%
}

\RequirePackage{pageslts}

%% Modify the section headers:
\RequirePackage[tiny,noindentafter]{titlesec}
\titleformat{\section}{\bf\color{labreport@blue}}{\thesection}{0em}{}
\titlespacing{\section}{0pt}{*2}{*0}
\titleformat{\subsection}{\sl\color{labreport@blue}}{\thesubsection}{0em}{}
\titlespacing{\subsection}{0pt}{*1.4}{*0}
\titlespacing{\paragraph}{0pt}{*1}{*0}
\setcounter{secnumdepth}{-1}

%% Redefine \maketitle:
\RequirePackage{ifthen}
\newcommand{\labreport@rule}[1]{\par
  \bigskip\noindent\rule{#1}{0.6pt}\par \bigskip
}
\renewcommand{\maketitle}{%
  \pagenumbering{arabic}%
  \setcounter{page}{\labreport@firstpage}
  \twocolumn[%
    \vspace{1.2cm}
    \begin{flushright}
      \color{labreport@blue}\small
    %   \textbf{Nordic Machine Intelligence, vol.~\labreport@vol, 
    %     pp.~\labreport@firstpage--\lastpageref{VeryLastPage}, \labreport@year}\\
      \textbf{\labreport@course \\}
      \labreport@rec%~/ published \labreport@publ%
    %   \ifthenelse{\equal{\labreport@doi}{0}}{}{\\
    %     \url{https://doi.org/10.2478/nmi-\labreport@doi}}
    \end{flushright}
    \vspace{3mm}
    \begin{NoHyper}
      \begin{minipage}{0.7\textwidth}
        \raggedright 
        {\fontsize{25}{30pt}\fontseries{sb}\selectfont
          \color{labreport@blue}\@title\par}

        \bigskip
        \renewcommand{\and}{, }
        \def \@makefntext##1{\@thefnmark. \textit{##1}}
        \renewcommand{\footnoterule}{}
        \renewcommand{\thempfootnote}{\arabic{mpfootnote}}
        \@author
      \end{minipage}
    \end{NoHyper}
    \labreport@rule{\textwidth}
  ]
  \thispagestyle{plain}
}

%% Redefine 'abstract':
\renewenvironment{abstract}
  {\section*{\abstractname}%\small
  }
  {\labreport@rule{\columnwidth}}

%% Reduce font size in the bibliography:
\AtBeginDocument{\renewcommand{\bibfont}{\normalfont\small}}

%% Viljar vil ha en kommando for romertall
\newcommand{\romnum}[1]{\MakeUppercase{\romannumeral #1}}

%% Viljar mekker mer dritt
\newcommand{\note}[1]{\textcolor{red}{#1}}

\renewcommand{\vec}[1]{\ensuremath{\mathbf{#1}}}


%% Finally, introduce hypertext references:
\RequirePackage[colorlinks=false,pdfborder={0 0 0}]{hyperref}
\urlstyle{sf}

%% and code appenix stuff
\usepackage{listings}
\usepackage{xcolor}

\definecolor{commentsColor}{rgb}{0.497495, 0.497587, 0.497464}
\definecolor{keywordsColor}{rgb}{0.000000, 0.000000, 0.635294}
\definecolor{stringColor}{rgb}{0.558215, 0.000000, 0.135316}

\lstset{ %
  backgroundcolor=\color{white},   % choose the background color; you must add \usepackage{color} or \usepackage{xcolor}
  basicstyle=\footnotesize,        % the size of the fonts that are used for the code
  breakatwhitespace=false,         % sets if automatic breaks should only happen at whitespace
  breaklines=true,                 % sets automatic line breaking
  captionpos=b,                    % sets the caption-position to bottom
  commentstyle=\color{commentsColor}\textit,    % comment style
  deletekeywords={...},            % if you want to delete keywords from the given language
  escapeinside={\%*}{*)},          % if you want to add LaTeX within your code
  extendedchars=true,              % lets you use non-ASCII characters; for 8-bits encodings only, does not work with UTF-8
  frame=tb,	                   	   % adds a frame around the code
  keepspaces=true,                 % keeps spaces in text, useful for keeping indentation of code (possibly needs columns=flexible)
  keywordstyle=\color{keywordsColor}\bfseries,       % keyword style
  language=Python,                 % the language of the code (can be overrided per snippet)
  otherkeywords={*,...},           % if you want to add more keywords to the set
  numbers=left,                    % where to put the line-numbers; possible values are (none, left, right)
  numbersep=5pt,                   % how far the line-numbers are from the code
  numberstyle=\tiny\color{commentsColor}, % the style that is used for the line-numbers
  rulecolor=\color{black},         % if not set, the frame-color may be changed on line-breaks within not-black text (e.g. comments (green here))
  showspaces=false,                % show spaces everywhere adding particular underscores; it overrides 'showstringspaces'
  showstringspaces=false,          % underline spaces within strings only
  showtabs=false,                  % show tabs within strings adding particular underscores
  stepnumber=1,                    % the step between two line-numbers. If it's 1, each line will be numbered
  stringstyle=\color{stringColor}, % string literal style
  tabsize=2,	                   % sets default tabsize to 2 spaces
  title=\lstname,                  % show the filename of files included with \lstinputlisting; also try caption instead of title
  columns=fixed                    % Using fixed column width (for e.g. nice alignment)
}

\endinput
