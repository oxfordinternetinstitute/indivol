<?php
include ".config.php";

function dblogger ($userid, $section, $payload, $datetime)
{
	// Create connection
	global $servername,$username,$password,$dbname;

	$conn = new mysqli($servername, $username, $password, $dbname);

	//echo " servername: " . $servername . ", username: " . $username . ", pw: " . $password . ", dbname: " . $dbname;
	//echo ", userid: " . $userid . ", section: " . $section . ", payload: " . $payload . ", dt: " . $datetime;

	// Check connection
	if ($conn->connect_error) {
		throw new Exception('{"error":"Failed to connect to database: ' . $conn->connect_error . '"}');
		return $conn->connect_error;
	}

	// bind parameters and execute
	$stmt = $conn->prepare("INSERT INTO logging (userid, section, payload, datetime) VALUES (?, ?, ?, ?)");

	$stmt->bind_param('sssi', $userid, $section, $payload, $datetime);

	if (!$stmt->execute()) {
		throw new Exception('{"error": "Execute failed: (' . $stmt->errno . ') ' . $stmt->error . '"}');
	}

	$stmt->close();
	$conn->close();

	return true;
}


if ($_SERVER['REQUEST_METHOD'] == 'POST') 
{
	$userid=$_POST["user_id"];

	$section=$_POST["section"];

	//$payload=json_encode($_POST["payload"]);
	$payload=$_POST["payload"];

	$datetime=new DateTime();
	$datetime=$datetime->getTimestamp();

	dblogger($userid,$section,$payload,$datetime);

}


?>
