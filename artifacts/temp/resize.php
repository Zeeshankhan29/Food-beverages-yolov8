<?php


function resize($newWidth, $targetFile, $originalFile) {

    $info = getimagesize($originalFile);
    $mime = $info['mime'];

    switch ($mime) {
            case 'image/jpeg':
                    $image_create_func = 'imagecreatefromjpeg';
                    $image_save_func = 'imagejpeg';
                    $new_image_ext = 'jpg';
                    break;

            case 'image/png':
                    $image_create_func = 'imagecreatefrompng';
                    $image_save_func = 'imagepng';
                    $new_image_ext = 'png';
                    break;

            case 'image/gif':
                    $image_create_func = 'imagecreatefromgif';
                    $image_save_func = 'imagegif';
                    $new_image_ext = 'gif';
                    break;

            default: 
                    throw new Exception('Unknown image type.');
    }

    $img = $image_create_func($originalFile);
    list($width, $height) = getimagesize($originalFile);

    $newHeight = ($height / $width) * $newWidth;
    $tmp = imagecreatetruecolor($newWidth, $newHeight);
    imagecopyresampled($tmp, $img, 0, 0, 0, 0, $newWidth, $newHeight, $width, $height);

    if (file_exists($targetFile)) {
            unlink($targetFile);
    }
    $image_save_func($tmp, "$targetFile.$new_image_ext");
}

function resizeImage($sourcePath, $destinationPath, $newWidth, $newHeight) {
	
	// Get the image type using exif_imagetype
	$imageType = exif_imagetype($sourcePath);

	if ($imageType !== false) {
		switch ($imageType) {
			case IMAGETYPE_JPEG:
				echo 'The image is a JPEG = '. basename($sourcePath) . PHP_EOL;
				break;
			case IMAGETYPE_PNG:
				echo 'The image is a PNG = '. basename($sourcePath) . PHP_EOL;
				list($width, $height) = getimagesize($sourcePath);
				if($width != $newWidth && $height != $newHeight){
					$sourceImage = imagecreatefrompng($sourcePath);
					$destinationImage = imagecreatetruecolor($newWidth, $newHeight);
					
					imagecopyresampled($destinationImage, $sourceImage, 0, 0, 0, 0, $newWidth, $newHeight, $width, $height);
					
					imagepng($destinationImage, $destinationPath);
					
					imagedestroy($sourceImage);
					imagedestroy($destinationImage);
				}
				break;
			case IMAGETYPE_GIF:
				echo 'The image is a GIF = '. basename($sourcePath) . PHP_EOL;
				break;
			default:
				echo 'The image type is unknown = '. basename($sourcePath) . PHP_EOL;
				break;
		}
	} else {
		echo 'Unable to determine the image type = '. basename($sourcePath) . PHP_EOL;
	}	
	
}


function resizeImagesInDirectory($directory) {
	// Your regular expression pattern
	$pattern = '/(?:\.git|\.ipynb_checkpoints|ImageSets|JPEGImages|SegmentationClass|SegmentationObject)/i';
	$imgpattern = '/\.(png)$/i';
	if (!preg_match($pattern, $directory)) {
		$files = scandir($directory);
		foreach ($files as $file) {
			$filePath = $directory . '/' . $file;
			//echo $filePath . PHP_EOL;
			if (is_file($filePath) && preg_match($imgpattern, $filePath)) {
				//$outputPath = $directory . '/resized/' . $file;
				$outputPath = $directory . '/' . $file;
				//echo $outputPath . PHP_EOL;
				resizeImage($filePath, $outputPath, 640, 360);
			} elseif (is_dir($filePath) && $file !== '.' && $file !== '..') {
				$subdirectory = $directory . '/' . $file;
				resizeImagesInDirectory($subdirectory);
			}
		}		
    } else {
        echo "Rejected : $directory\n";
    }
	
}
$sourceDirectory = __DIR__;
/*
$sourceDirectory = __DIR__;
$destinationDirectory = $sourceDirectory . '/resized';

if (!is_dir($destinationDirectory)) {
    mkdir($destinationDirectory);
}

*/
resizeImagesInDirectory($sourceDirectory);

echo "Images resized successfully!";