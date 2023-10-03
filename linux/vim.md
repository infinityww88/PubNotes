That's because Vim is using $VIMRUNTIME/defaults.vim as the vimrc file.

If you look at :h .vimrc you'll see that Vim looks in five places for a vimrc file, stopping once it's found one.

When you have an empty personal vimrc (in your home directory, usually) then Vim will read that and stop searching. Obviously, if the file is empty there's no configuration of file type detection and, thus, no syntax highlighting.

When you don't have a personal vimrc then Vim continues down the list until it gets to the last item which is defaults.vim. This vimrc file includes filetype on and syntax on which enable file type detection and syntax highlighting, respectively.

source $VIMRUNTIME/defaults.vim   " Add this to your ~/.vimrc

习惯在 vim 用 help 命令学习 vim。

在 vim 命令模式下执行 :echo $VIMRUNTIME 显示 vim 的运行时目录，一般是 /usr/share/vim/vim90/

To get a block cursor in Vim in the Cygwin/msys2 terminal write following code in .vimrc file

let &t_ti.="\e[1 q"
let &t_SI.="\e[5 q"
let &t_EI.="\e[1 q"
let &t_te.="\e[0 q"

