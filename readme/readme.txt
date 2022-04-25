Plugin for CudaText
Saves cursor position for temporary files

The idea behind this small plugin. On Unix, you open some file from FTP plugin. File is downloaded to temp dir, and CudaText opens it from there, file name is like /tmp/someFIRSTprefix/dir/file.txt . Now you close it, and open file in FTP again. CudaText opens it from another dir now: /tmp/someOTHERprefix/dir/file.txt. With plugin, you can keep caret position in the file, even if CudaText opens temp file from a different dir (that dir is calculated by Python and has some random prefix).

Author: ildar r. khasanshin (github.com/ildarkhasanshin)
License: MIT