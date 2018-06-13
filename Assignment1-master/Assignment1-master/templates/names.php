<html lang="en">

<head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" crossorigin="anonymous">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" crossorigin="anonymous">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" crossorigin="anonymous"></script>

</head>

<body>
    <div id="wrap">
        <div class="container">
            <div class="row">
                <center>
                            S<h2>Ilwin Joey Dcunha</h2><br>
                            <h2>1001390458</h2>
                            <img src=" {{url_for('static', filename='ilwin.jpg')}}" height="300" width="300" alt="No Image Available">
                        </center>
                        <br>
                        <br>
                <form class="form-horizontal" action="/search" method="post" name="upload_excel" >
                   <lable>Course range1 </lable> <input type="text" name="range1">
                   <lable>Course range2 </lable> <input type="text" name="range2">

                   <button type="submit" id="submit" name="Import" class="btn btn-primary button-loading" data-loading-text="Loading...">Submit</button>
                </form>
            </div>
            <?php
               get_all_records();
            ?>
        </div>
    </div>
</body>

</html>