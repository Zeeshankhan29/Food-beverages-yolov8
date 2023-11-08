<?php
$sourceFile = __DIR__ . '/copyclasses.php';

$destinationDirectories = [
	"Apple Granny Smith",
	"Apple Royal Gala",
	"Apple Shimla",
	"Ash Gourd Cut",
	"Avocado Indian",
	"Banana Flower",
	"Banana Hills",
	"Banana Morris",
	"Banana Nendran",
	"Banana Poovan",
	"Banana Rasthali",
	"Banana Red",
	"Bitter Gourd",
	"Bok Choy",
	"Bottle Gourd",
	"Brinjal Black Big",
	"Brinjal Long",
	"Brinjal Purple Striped",
	"Broccoli",
	"Cabbage",
	"Cabbage Red",
	"Capsicum",
	"Capsicum Red",
	"Capsicum Yellow",
	"Cauliflower",
	"Chilli Long Bajji",
	"Chinese Cabbage",
	"Coconut",
	"Coconut Flower",
	"Cucumber",
	"Custard Apple",
	"Dragon Fruit Red",
	"Golden Kiwi",
	"Gooseberry Amla",
	"Guava White",
	"Jackfruit raw",
	"Kiwi Green",
	"Lemon",
	"Mango Neelam",
	"Mango Totapuri",
	"Mangusteens Indian",
	"Mosambi",
	"Muskmelon Rock",
	"Muskmelon Yellow",
	"Nectarines",
	"Onion Big Bellary",
	"Orange Valencia",
	"Papaya",
	"Pineapple",
	"Pomegranate Kabul",
	"Pumpkin",
	"Pumpkin cut Wrapped",
	"Radish Red",
	"Radish White",
	"Sapota Round",
	"Snake Gourd",
	"Tomato Apple",
	"Tomato Nadu",
	"Turnip",
	"Watermelon Kiran",
	"Zucchini Green",
	"Zucchini Yellow",
];

foreach ($destinationDirectories as $destinationDirectory) {
    $destinationPath = __DIR__ . DIRECTORY_SEPARATOR . rtrim($destinationDirectory, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . basename($sourceFile);
    
    if (copy($sourceFile, $destinationPath)) {
        echo "File copied to $destinationDirectory\n";
    } else {
        echo "Failed to copy to $destinationDirectory\n";
    }
}

echo "Files copied to all directories.";