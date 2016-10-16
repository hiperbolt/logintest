<!--HTML SECTION-->
<h2>Recover password:</h2>
<form method="post" action="index.php">
    Recovery Code:<br>
    <input type="text" name="enteredrecoverycode">
    <br>
    New Password:<br>
    (Make Sure to have NO spaces!)<br>
    <input type="text" name="newpassword">
    <br><br>
    <input type="submit" value="Confirm!" name="submit"> <!-- assign a name for the button -->
</form>

<?php
// Main Function
function main()
{
    $servername = "";
    $username = "";
    $password = "";
    $dbname = "logininfo";
    $conn = new mysqli($servername, $username, $password, $dbname);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $sql = sprintf("SELECT recoverycode FROM passwordrecover WHERE recoverycode= %s",$_POST["enteredrecoverycode"]);
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        exec('python htmltest.py ' . $_POST["enteredrecoverycode"] . ' ' . $_POST["newpassword"]);
    }
   echo "Sucess!"
} else {
    echo "/Wrong recovery code, please try again!";
}
$conn->close();
}

// Detect Form Submit and Call main function
if(isset($_POST['submit']))
{
   main();
}
?>


