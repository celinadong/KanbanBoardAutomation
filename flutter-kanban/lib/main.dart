import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'image_picker_channel.dart';
import 'package:http/http.dart' as http;
import 'dart:developer';
import 'package:flutter/foundation.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:image/image.dart' as Img;
import 'package:path_provider/path_provider.dart';

// import 'package:image_picker_modern/image_picker_modern.dart';

void main() => runApp(new MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      title: 'Kanban Sync Demo',
      theme: new ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: new MyHomePage(title: 'Kanban Synchro Demo'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => new _MyHomePageState();
}


class _MyHomePageState extends State<MyHomePage> {

  ImagePicker _imagePicker = new ImagePickerChannel();

  File _imageFile;

  void captureImage(ImageSource captureMode) async {
    try {
      var imageFile = await _imagePicker.pickImage(imageSource: captureMode);
      setState(() {
        _imageFile = imageFile;
      });
    }
    catch (e) {
      print(e);
    }
  }

  Widget _buildImage() {
    if (_imageFile != null) {
      return new Image.file(_imageFile);
    } else {
      return new Text('Take an image to start', style: new TextStyle(fontSize: 18.0));
    }
  }

void _onLoading() {
  showDialog(
    context: context,
    barrierDismissible: false,
    child: new Dialog(
      child: new Column(
        mainAxisSize: MainAxisSize.min,
        children:[
          new Container(height: 20,),
          new Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              new CircularProgressIndicator(),
              new Container(width: 50,),
              new Text("Processing"),
            ],
          ),
          new Container(height: 20,),
        ],
      ),
    ),
  );
}
  // Future<String> get _localPath async {
  //   final directory = await getApplicationDocumentsDirectory();

  //   return directory.path;
  // }
  void _submitImage(){
    print("_submitImage called");
    
    if (_imageFile == null) return;

    _onLoading();
    // Img.Image image_temp = Img.decodeImage(_imageFile.readAsBytesSync());
    // Img.Image resized_img = Img.copyResize(image_temp, height:700);
    // File resizedFile = new File('$path/${DateTime.now().toUtc().toIso8601String()}.png')
      // ..writeAsBytesSync(Img.encodePng(resized_img));
    // Image tempImage = decodeImage(_imageFile);
    // Image reducedImage = copyResize(tempImage, 120);
    
    String base64Image = base64Encode(_imageFile.readAsBytesSync());
    // String fileName = _imageFile.path.split("/").last;

    String endPoint = "http://77.68.87.207:1997/getText";
    // String endPoint = "http://localhost:1997/getText";

    http.post(endPoint, body: base64Image)
    .then((res) {
      Navigator.of(context).pop();
      print("request reached with status code : " + res.statusCode.toString());
      if(res.statusCode == 200)
        _showDialog("Succeed");
      else
        _showDialog("Failed. Please Try Again.");
    }).catchError((err) {
      Navigator.of(context).pop();
      print(err);
    });

    print("posted");
  }

  @override
  Widget build(BuildContext context) {
    return new Scaffold(
      appBar: new AppBar(
        title: new Text(widget.title),
      ),
      body: new Column(
        children: [
          new Expanded(child: new Center(child: _buildImage())),
          _buildButtons(),
        ]
      ),
    );
  }


  Widget _buildButtons() {
    return new ConstrainedBox(
      constraints: BoxConstraints.expand(height: 80.0),
      child: new Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: <Widget>[
          _buildActionButton(new Key('retake'), 'Photos', () => captureImage(ImageSource.photos)),
          _buildActionButton(new Key('upload'), 'Camera', () => captureImage(ImageSource.camera)),
          _buildActionButton(new Key('submit'), 'Submit', () => _submitImage()),
        ]
      ));
  }

  Widget _buildActionButton(Key key, String text, Function onPressed) {
    return new Expanded(
      child: new FlatButton(
          key: key,
          child: new Text(text, style: new TextStyle(fontSize: 20.0)),
          shape: new RoundedRectangleBorder(),
          color: Colors.blueAccent,
          textColor: Colors.white,
          onPressed: onPressed),
    );
  }

  void _showDialog(String promptText) {
    // flutter defined function
    showDialog(
      context: context,
      builder: (BuildContext context) {
        // return object of type Dialog
        return AlertDialog(
          title: new Text("Syncronisation Result"),
          content: new Text(promptText),
          actions: <Widget>[
            // usually buttons at the bottom of the dialog
            new FlatButton(
              child: new Text("Close"),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
            new FlatButton(
              child: new Text("Go to Board"),
              onPressed: (){
                launch("https://github.com/VaniOFX/GlobalHackathon/projects/1");
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }
}


