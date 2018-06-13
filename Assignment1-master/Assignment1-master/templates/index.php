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
                <h1>Ilwin Dcunha</h1>
                     <br>
                <h2>1001390458</h2>

                <form class="form-horizontal" action="/uploadCSV" method="post" name="upload_excel" enctype="multipart/form-data">
                    <fieldset>

                        <!-- File Button -->
                        <div class="form-group">
                            <label class="col-md-4 control-label" for="filebutton">Select File</label>
                            <div class="col-md-4">
                                <input type="file" name="file" id="file1" class="input-large">
                            </div>
                        </div>

                        <!-- Button -->
                        <div class="form-group">
                            <label class="col-md-4 control-label" for="singlebutton">Import data</label>
                            <div class="col-md-4">
                                <button type="submit" id="submit" name="Import" class="btn btn-primary button-loading" data-loading-text="Loading...">Import</button>
                            </div>

                        </div>
                         <h2>File size {{ variable }}</h2>

                        <a href="/UI"> click here for UI</a>
                        <br>
                        <a href="/earthquake"> click here for Earthquakes</a>
                         <br>
                         <a href="/cluster"> click here for cluster </a>
                        <br>
                         <strong>   Do large (>4.0 mag) occur more often at night? </strong>
                         <b><a href="/question">  Click </a> to find out.<br>
                         <b> Ans: {{res}}

                    </fieldset>
                </form>

            </div>
            <?php
               get_all_records();
            ?>
        </div>
    </div>
</body>

</html>