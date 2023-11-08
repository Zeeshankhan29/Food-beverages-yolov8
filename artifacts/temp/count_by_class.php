<?php

$classes = [
'Apple Royal Gala',
'Apple Shimla',
'Ash Gourd Cut',
'Avocado',
'Banana Nendran',
'Banana Poovan',
'Banana Red',
'Brinjal Black Big',
'Brinjal Purple Striped',
'Broccoli',
'Cabbage Red',
'Cabbage_',
'Capsicum Red',
'Capsicum Yellow',
'Capsicum_',
'Cauliflower',
'Cucumber',
'Dragon Fruits Red',
'Golden Kiwi',
'Jackfruit Raw',
'Kiwi Green',
'Lemon',
'Mango Neelam',
'Mango Totapuri',
'Mangusteens Indian',
'Mosambi',
'Muskmelon Rock',
'Musk Melon Yellow',
'Orange Valencia',
'Papaya',
'Pineapple',
'Pomegranate Kabul',
'Pumpkin cut Wrapped',
'Radish Red',
'Sapota Round',
'Tomato Apple',
'Tomato Nadu',
'Turnip',
'Watermelon Kiran'
];
$class_count = [];

function classCountIndirectory($directory,$classregex,&$class_count) {
    $files = scandir($directory);
    foreach ($files as $file) {
        $filePath = $directory . '/' . $file;
        //echo $filePath . PHP_EOL;
        if (is_file($filePath)) {
            preg_match($classregex, $filePath, $matches) . PHP_EOL;
            //echo $classregex.PHP_EOL;
            $newmatches = array_shift($matches);
            array_push($class_count, $newmatches);
        } elseif (is_dir($filePath) && $file !== '.' && $file !== '..') {
            $subdirectory = $directory . '/' . $file;
            classCountIndirectory($subdirectory,$classregex,$class_count);
        }
        //echo PHP_EOL;
    }
}

if(!isset($argv[1])){
	echo "Need Directory to find the count". PHP_EOL;
	exit(0);
}
$classregex = '/(' . implode(')|(',$classes) . ')/i';
classCountIndirectory($argv[1], $classregex, $class_count);
$vals = array_count_values(array_values(array_filter($class_count)));
print_r($vals);
