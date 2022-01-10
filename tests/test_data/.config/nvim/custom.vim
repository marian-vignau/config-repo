call plug#begin('~/.vim/plugged')
Plug 'vim-ctrlspace/vim-ctrlspace'
Plug 'psf/black', { 'tag': '19.10b0' }
Plug 'lukas-reineke/indent-blankline.nvim'
call plug#end()
let g:black_linelength = 120
" required for vim-ctrlspace
set nocompatible
set hidden
set encoding=utf-8
" let g:airline#extensions#ctrlspace#enabled = 1
" let g:CtrlSpaceStatuslineFunction = "airline#extensions#ctrlspace#statusline()" line()" 
let g:CtrlSpaceDefaultMappingKey = "<C-space> "
nnoremap <silent><C-p> :CtrlSpace O<CR>
" use s key to delete, not cut
nnoremap s "_d
nnoremap ñ :CtrlSpace<CR>
" custom copy, cut & paste from/to system's clipboard -- paste is L for before, ; for after,
" both in normal and insert modes
map <C-K> "+y<C-M>
map <C-X> "+d<C-M>
map <C-L> "+P
imap <C-L> <C-O>"+P
map <C-;> "+p
imap <C-;> <C-O>"+p

" Using <Tab> as <Esc>,https://vim.fandom.com/wiki/Avoid_the_escape_key 
nnoremap <Tab> <Esc>
vnoremap <Tab> <Esc>gV
onoremap <Tab> <Esc>
cnoremap <Tab> <C-C><Esc>
inoremap <Tab> <Esc>`^
inoremap <Leader><Tab> <Tab>
" Navegate one tab left or one tab right 
" using space bar, arrow key
"map <space><Right> :tabn<CR>
"imap <space><Right> <ESC>:tabn<CR>
"map <space><Left> :tabp<CR>
"imap <space><Left> <ESC>:tabp<CR>

" Beautiful fzf
" View old files
nnoremap ,h         :History<CR>
" Git blame
nnoremap ,b         :BCommits<CR>
" Shortcuts
nnoremap ,A         :Maps<CR>
" Show YankRing
nnoremap ,y         :YRShow<CR>
" Search on YankRing
nnoremap ,Y         :YRSearch
" Open CtrlSpace 
nnoremap ,<SPACE>   :CtrlSpace<CR>
" Change tabs
nnoremap ,,1        :tabn 1<CR>
nnoremap ,,2        :tabn 2<CR>
nnoremap ,,3        :tabn 3<CR>
nnoremap ,,4        :tabn 4<CR>
nnoremap ,,5        :tabn 5<CR>
nnoremap ,,6        :tabn 6<CR>
nnoremap ,,7        :tabn 7<CR>
nnoremap ,,8        :tabn 8<CR>
nnoremap ,,9        :tabn 9<CR>
nnoremap ,,<        :tabfirst<CR>
nnoremap ,,-        :tablast<CR>
nnoremap ,,q        :tabclose<CR>
nnoremap ,,}        :tabnext<CR>
nnoremap ,,{        :tabprevious<CR>
nnoremap <bar><bar> :vs<CR>
" Override configs by directory
" Plug 'xolox/vim-misc'
" Plug 'xolox/vim-session'
function NoBreakpoint()
    :g/import.*pdb.*set_trace()/de
    :g/.pdb\.set_trace()/de
    :g/import .pdb/de
    :g/import.*pudb.*set_trace()/de     
    :g/import.*pudb.*pu.db/de     
    :g/breakpoint()/de     
endfunction

function Pre()
    :Black
    :Isort 
    :wr
endfunction

function! s:ToggleBlame()
    if &l:filetype ==# 'fugitiveblame'
        close
    else
        G blame
    endif
endfunction

nnoremap gb :call <SID>ToggleBlame()<CR>

map <silent> <F9> <ESC>:call Pre()<CR>
map <silent> <S-F9> <ESC>:call NoBreakpoint()<CR>:call Pre()<CR>

