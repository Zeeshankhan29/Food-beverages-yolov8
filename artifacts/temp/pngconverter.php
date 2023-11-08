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

function pngconverter($sourcePath){
	
	// Get the image type using exif_imagetype
	$imageType = exif_imagetype($sourcePath);
	$imgpattern = '/\.(jpg|jpeg|png|gif|bmp)$/i';
	
	if ($imageType !== false) {
		switch ($imageType) {
			case IMAGETYPE_JPEG:
				echo 'The image is a JPEG = '. basename($sourcePath) . PHP_EOL;
				// Load the JPEG image
				$jpegImage = imagecreatefromjpeg($sourcePath);

				if ($jpegImage === false) {
					die('Unable to load the JPEG image.');
				}

				// Create a new PNG image with the same dimensions
				$pngImage = imagecreatetruecolor(imagesx($jpegImage), imagesy($jpegImage));

				// Preserve transparency for PNG images (if needed)
				imagealphablending($pngImage, false);
				imagesavealpha($pngImage, true);

				// Fill the PNG image with a transparent background
				$transparentColor = imagecolorallocatealpha($pngImage, 0, 0, 0, 127);
				imagefill($pngImage, 0, 0, $transparentColor);

				// Copy the JPEG image onto the PNG image
				imagecopy($pngImage, $jpegImage, 0, 0, 0, 0, imagesx($jpegImage), imagesy($jpegImage));

				// Save the PNG image to a file
				$pngPath = preg_replace($imgpattern, '.png', $sourcePath);
				imagepng($pngImage, $pngPath);

				// Free up memory by destroying the image resources
				imagedestroy($jpegImage);
				imagedestroy($pngImage);

				echo 'Conversion complete. Image saved as ' . $pngPath . PHP_EOL;
				break;
			case IMAGETYPE_BMP:
				echo 'The image is a BMP = '. basename($sourcePath) . PHP_EOL;
				// Load the BMP image
				$bmpPath = $sourcePath;
				$bmpImage = imagecreatefrombmp($bmpPath);

				if ($bmpImage === false) {
					die('Unable to load the BMP image.');
				}

				// Create a new PNG image with the same dimensions
				$pngImage = imagecreatetruecolor(imagesx($bmpImage), imagesy($bmpImage));

				// Preserve transparency for PNG images (if needed)
				imagealphablending($pngImage, false);
				imagesavealpha($pngImage, true);

				// Fill the PNG image with a transparent background
				$transparentColor = imagecolorallocatealpha($pngImage, 0, 0, 0, 127);
				imagefill($pngImage, 0, 0, $transparentColor);

				// Copy the BMP image onto the PNG image
				imagecopy($pngImage, $bmpImage, 0, 0, 0, 0, imagesx($bmpImage), imagesy($bmpImage));

				// Save the PNG image to a file
				$pngPath = preg_replace($imgpattern, '.png', $sourcePath);
				imagepng($pngImage, $pngPath);

				// Free up memory by destroying the image resources
				imagedestroy($bmpImage);
				imagedestroy($pngImage);

				echo 'Conversion complete. Image saved as ' . $pngPath . PHP_EOL;
				
				break;
			case IMAGETYPE_GIF:
				echo 'The image is a GIF = '. basename($sourcePath) . PHP_EOL;
				// Load the GIF image
				$gifPath = $sourcePath;
				$gifImage = imagecreatefromgif($gifPath);

				if ($gifImage === false) {
					die('Unable to load the GIF image.');
				}

				// Create a new PNG image with the same dimensions
				$pngImage = imagecreatetruecolor(imagesx($gifImage), imagesy($gifImage));

				// Preserve transparency for PNG images (if needed)
				imagealphablending($pngImage, false);
				imagesavealpha($pngImage, true);

				// Fill the PNG image with a transparent background
				$transparentColor = imagecolorallocatealpha($pngImage, 0, 0, 0, 127);
				imagefill($pngImage, 0, 0, $transparentColor);

				// Copy the GIF image onto the PNG image
				imagecopy($pngImage, $gifImage, 0, 0, 0, 0, imagesx($gifImage), imagesy($gifImage));

				// Save the PNG image to a file
				$pngPath = preg_replace($imgpattern, '.png', $sourcePath);
				imagepng($pngImage, $pngPath);

				// Free up memory by destroying the image resources
				imagedestroy($gifImage);
				imagedestroy($pngImage);

				echo 'Conversion complete. Image saved as ' . $pngPath . PHP_EOL;
				break;
			case IMAGETYPE_PNG:
				echo 'The image is a PNG = '. basename($sourcePath) . PHP_EOL;
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
	$imgpattern = '/\.(jpg|jpeg|png|gif|bmp)$/i';
	if (!preg_match($pattern, $directory)) {
		$files = scandir($directory);
		foreach ($files as $file) {
			$filePath = $directory . '/' . $file;
			//echo $filePath . PHP_EOL;
			if (is_file($filePath) && preg_match($imgpattern, $filePath)) {
				//$outputPath = $directory . '/resized/' . $file;
				$outputPath = $directory . '/' . $file;
				//echo $outputPath . PHP_EOL;
				pngconverter($filePath);
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