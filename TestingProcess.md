# Testing Process

1. Check about dialog. The icon should be present and the link to my site should send you to https://ottop.eu. The license link should send you to https://opensource.org/license/mit/ Check credits tab also.
2. Try to run without including any files. The progress window should say "Error: You are missing a file or there's an issue with the files". 
3. Try to run with only an image and then with only audio. Result should be as above.
4. Try to run validly with an image and an audio file. Should successfully create a video that combines them.
5. Try running it without adding files again after the successful run. Should be similar to case 2.
6. Try to run with valid files, but save in a directory without write access. The progress window should say "Error: Unable to write to {Path that you tried to save it to}".
7. Do everything validly, but name the extension with a non-mp4 extension, such as avi. Should still be an mp4 file (your file manager may misread this due to the extension, but that is not necessarily the real file type).
8. Try to run with an image or audio file that you don't have read access to. Should not break the program in any functional way, but gives the error message "Error: Unable to write to {Path that you tried to save it to}" due to the lack of earlier handling, so it needs to be updated for a later release.
9. Start a valid run, but then click on the exit button of the progress dialog in the middle of processing. The processing should stop and the uncompleted output file should be deleted.