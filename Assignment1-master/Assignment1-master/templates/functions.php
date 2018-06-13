<?php


 if(isset($_POST["Import"])){

		$filename=$_FILES["file"]["tmp_name"];

        $dbhandle = sqlite_open('imageDb.db');
		 if($_FILES["file"]["size"] > 0)
		 {
		  	$file = fopen($filename, "r");
	        while (($getData = fgetcsv($file, 10000, ",")) !== FALSE)
	         {


	           $sql = "INSERT into Picture (name,grade,room,telnum,picture,keywords)
                   values ('".$getData[0]."','".$getData[1]."','".$getData[2]."','".$getData[3]."','".$getData[4]."','".$getData[5]."')";

               $result = sqlite_exec($dbhandle, $sql , $error);
				if($result)
				{
					echo "<script type=\"text/javascript\">
							alert(\"Invalid File:Please Upload CSV File.\");
							window.location = \"index.php\"
						  </script>";
				}
				else {
					  echo "<script type=\"text/javascript\">
						alert(\"CSV File has been successfully Imported.\");
						window.location = \"index.php\"
					</script>";
				}
	         }

	         fclose($file);
		 }
	}


 ?>