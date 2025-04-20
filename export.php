<?php 
if ($_SERVER['REQUEST_METHOD'] == 'POST') { 
    // Collect form data 
    $name = $_POST['name']; 
    $sys = $_POST['sys']; 
    $dia = $_POST['dia'];
    $pul = $_POST['pul'];
 
    // Create a CSV file 
    $filename = "data.csv"; 
    $file = fopen($filename, "a"); // Open the file in append mode 
    // Prepare the data to be written 

    
    $data = [$name, $sys, $dia, $pul]; 
 
    // Write the data to the CSV file 
    fputcsv($file, $data); 
 
    // Close the file 
    fclose($file); 
 
    // Provide feedback to the user 
    echo "Data exported successfully to $filename."; 
} else { 
    echo "No data submitted."; 
} 
?> 
