<?php
$incluideclasses = [
	'Apple Granny Smith',
	'Apple Royal Gala',
	'Apple Shimla',
	'Ash Gourd Cut',
	'Avocado Indian',
	'Banana Flower',
	'Banana Hills',
	'Banana Morris',
	'Banana Nendran',
	'Banana Poovan',
	'Banana Rasthali',
	'Banana Red',
	'Bitter Gourd',
	'Bok Choy',
	'Bottle Gourd',
	'Brinjal Black Big',
	'Brinjal Long',
	'Brinjal Purple Striped',
	'Broccoli',
	'Cabbage',
	'Cabbage Red',
	'Capsicum',
	'Capsicum Red',
	'Capsicum Yellow',
	'Cauliflower',
	'Chilli Long Bajji',
	'Chinese Cabbage',
	'Coconut',
	'Coconut Flower',
	'Cucumber',
	'Custard Apple',
	'Dragon Fruit Red',
	'Golden Kiwi',
	'Gooseberry Amla',
	'Guava White',
	'Jackfruit raw',
	'Kiwi Green',
	'Lemon',
	'Mango Neelam',
	'Mango Totapuri',
	'Mangusteens Indian',
	'Mosambi',
	'Muskmelon Rock',
	'Muskmelon Yellow',
	'Nectarines',
	'Onion Big Bellary',
	'Orange Valencia',
	'Papaya',
	'Pineapple',
	'Pomegranate Kabul',
	'Pumpkin',
	'Pumpkin cut Wrapped',
	'Radish Red',
	'Radish White',
	'Sapota Round',
	'Snake Gourd',
	'Tomato Apple',
	'Tomato Nadu',
	'Turnip',
	'Watermelon Kiran',
	'Zucchini Green',
	'Zucchini Yellow'
];

$excludeclasses = [
	'Apple Fuji',
	'Chow Chow',
	'Potato'
];
$incluideclassespattern = '/('.implode(')|(', $incluideclasses).')/i';
//ECHO $incluideclassespattern . PHP_EOL;
//EXIT(0);
//echo implode("|", $excludeclasses) . PHP_EOL;
$pattern = '/(?:\.git|\.ipynb_checkpoints|ImageSets|SegmentationObject|'.implode("|", $excludeclasses).')/i';
$maskpattern = '/(?:segment)/i';
$originalpattern = '/(?:image)/i';
$imgpattern = '/\.(png)$/i';

function recursiveDirectoryCopy($source, $destination) {
	global $incluideclasses,$excludeclasses,$pattern,$maskpattern,$originalpattern,$imgpattern,$incluideclassespattern;
    if (!is_dir($source)) {
        return false;
    }
    
    if (!is_dir($destination)) {
        mkdir($destination, 0777, true);
    }
    
    $dir = new DirectoryIterator($source);
    foreach ($dir as $fileInfo) {
        if ($fileInfo->isFile() && strtolower($fileInfo->getExtension()) === 'png') {
			$fn = $fileInfo->getFilename();
			$pn = $fileInfo->getPathname();
			//echo $fn . PHP_EOL;
			//echo $fileInfo->getBasename() . PHP_EOL;
			$matches = [];
			if (preg_match($incluideclassespattern, $pn, $matches)) {
				// Remove blank values from the array
				$filteredArray = array_filter($matches, function ($value) {
					// Use strict comparison to check for emptiness
					return !empty($value);
				});

				// Reindex the array if you want to reset keys
				$filteredArray = array_values(array_unique($filteredArray));
				$filefn = "";
				if (preg_match($maskpattern, $pn)) {
					if(preg_match($imgpattern, $fn)){
						$filefn =  $destination . DIRECTORY_SEPARATOR . 'mask'  . DIRECTORY_SEPARATOR . implode("",$filteredArray) . DIRECTORY_SEPARATOR . $fn;
						echo $pn .' =>  ' . $filefn . PHP_EOL;
					}
				}
				if (preg_match($originalpattern, $pn)) {
					if(preg_match($imgpattern, $fn)){
						$filefn = $destination . DIRECTORY_SEPARATOR .'original' . DIRECTORY_SEPARATOR . implode("",$filteredArray) . DIRECTORY_SEPARATOR . $fn;
						echo $pn .' =>  ' . $filefn . PHP_EOL;
					}
				}
				copy($pn, $filefn);
			}
        }
		if ($fileInfo->isDir() && !$fileInfo->isDot()) {
			$fn = $fileInfo->getFilename();
			$pn = $fileInfo->getPathname();
			if (!preg_match($pattern, $fn)) {
				$matches = [];
				$dstdir =  $destination;
				if (preg_match($incluideclassespattern, $pn, $matches)) {
					// Remove blank values from the array
					$filteredArray = array_filter($matches, function ($value) {
						// Use strict comparison to check for emptiness
						return !empty($value);
					});

					// Reindex the array if you want to reset keys
					$filteredArray = array_values(array_unique($filteredArray));
					if (preg_match($maskpattern, $pn)) {
						$dstdir =  $destination . DIRECTORY_SEPARATOR . 'mask'  . DIRECTORY_SEPARATOR . implode("",$filteredArray) . DIRECTORY_SEPARATOR;
					}
					if (preg_match($originalpattern, $pn)) {
						$dstdir = $destination . DIRECTORY_SEPARATOR .'original' . DIRECTORY_SEPARATOR . implode("",$filteredArray) . DIRECTORY_SEPARATOR;
					}
					if (!is_dir($dstdir)) {
						mkdir($dstdir, 0777, true);
					}
				}				
				recursiveDirectoryCopy($fileInfo->getPathname(), $destination);
			}
        }
    }
}

$sourceDirectory = __DIR__;
$destinationDirectory = 'F:\DEV-PYTHON\self-checkout\artifacts\temp';

recursiveDirectoryCopy($sourceDirectory, $destinationDirectory);

echo 'Directory and PNG files copied successfully.';


?>
