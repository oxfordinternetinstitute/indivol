<?php
include ".config.php";

function dbloader ($userid)
{
	// Create connection
	global $servername,$username,$password,$dbname;

	$conn = new mysqli($servername, $username, $password, $dbname);

	// Check connection
	if ($conn->connect_error) {
		throw new Exception('{"error":"Failed to connect to database: ' . $conn->connect_error . '"}');
		return $conn->connect_error;
	}

	// bind parameters and execute

	$stmt = $conn->prepare("SELECT percentages FROM socinfo WHERE userid = ?");

	$stmt->bind_param('s', $userid);

	$stmt->execute();

	if (!stmt) {
		throw new Exception('{"error": "Execute failed: (' . $stmt->errno . ') ' . $stmt->error . '"}');
	}

	$stmt->bind_result($percentages);
	$stmt->fetch();

	$output=$percentages;

	$stmt->close();
	$conn->close();

	return $output;
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') 
{
	$userid=$_POST["user_id"];
	$output = dbloader($userid);
	echo json_encode($output);
}

?>
