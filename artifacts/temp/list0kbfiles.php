<?php



function listZeroKBImages($directory) {
    if ($handle = opendir($directory)) {
        while (false !== ($file = readdir($handle))) {
            if ($file != "." && $file != "..") {
                $filePath = $directory . '/' . $file;

                if (is_dir($filePath)) {
                    // If the item is a directory, recursively search it
                    listZeroKBImages($filePath);
                } else {
                    // Check if the file is a regular file and ends with a known image file extension
                    if (is_file($filePath) && preg_match('/\.(jpg|jpeg|png|gif|bmp)$/i', $file)) {
                        // Get the file size in bytes
                        $fileSize = filesize($filePath);

                        // Check if the file size is 0KB
                        if ($fileSize === 0) {
                            echo "0KB Image File: " . $filePath . PHP_EOL;
                        }
                    }
                }
            }
        }
        closedir($handle);
    }
}

$directory =  __DIR__;
listZeroKBImages($directory);
