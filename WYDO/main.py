import os
from twisted.internet import threads, defer
from twisted.internet.protocol import ProcessProtocol
from twisted.python import failure
from PIL import Image
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserController

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView

class FileUploadDialog(BoxLayout):
    def __init__(self, app):
        super().__init__(orientation='vertical')
        self.app = app
        self.add_widget(Label(text='Select a file to upload:'))

        self.file_chooser = FileChooserListView()
        self.file_chooser.bind(on_selection=self.on_file_selected)
        self.add_widget(self.file_chooser)

    def on_file_selected(self, file_chooser, selection):
        if selection:
            self.app.upload_file(selection[0])
            self.dismiss()

class ScanProcessProtocol(ProcessProtocol):
    def __init__(self, deferred, scan_command, output_filename):
        self.deferred = deferred
        self.scan_command = scan_command
        self.output_filename = output_filename

    def connectionMade(self):
        self.transport.write(self.scan_command)

    def outReceived(self, data):
        print("Scanning process output: ", data)

    def processEnded(self, reason):
        if reason.check(failure.Failure):
            self.deferred.errback(reason)
        else:
            self.deferred.callback(self.output_filename)


class ImageScannerApp(App):
    def build(self):
        self.title = 'WYDO'
        self.icon = 'scanner.png'
        self.use_kivy_settings = False

        Window.clearcolor = (1, 1, 1, 1)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.scan_button = Button(text='Scan', size_hint=(1, 0.25))
        self.scan_button.bind(on_press=self.scan_image)
        layout.add_widget(self.scan_button)

        self.image_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.5))
        layout.add_widget(self.image_box)

        return layout
    

    def scan_image(self, instance):
        self.scan_button.disabled = True
        scan_command = "scanimage -x 210 -y 297 --mode Color --source 'Automatic Document Feeder(left aligned,Duplex)' --format pnm > scan.pnm"
        d = threads.deferToThread(os.system, scan_command)
        d.addCallback(self.process_scan_image)
        d.addErrback(self.scan_error)
        d.addBoth(self.enable_scan_button)

        # Open file dialog to select file for upload
        file_dialog = FileUploadDialog(self)
        file_dialog.open()

    # def scan_image(self, instance):
    #     self.scan_button.disabled = True
    #     scan_command = "scanimage -x 210 -y 297 --mode Color --source 'Automatic Document Feeder(left aligned,Duplex)' --format pnm > scan.pnm"
    #     d = threads.deferToThread(os.system, scan_command)
    #     d.addCallback(self.process_scan_image)
    #     d.addErrback(self.scan_error)
    #     d.addBoth(self.enable_scan_button)

    #     # Upload the file after scanning
    #     d_upload = threads.deferToThread(self.upload_file, 'scan.pnm')
    #     d_upload.addCallback(self.upload_success)
    #     d_upload.addErrback(self.upload_error)

    # def scan_image(self, instance):
        self.scan_button.disabled = True
        scan_command = "scanimage -x 210 -y 297 --mode Color --source 'Automatic Document Feeder(left aligned,Duplex)' --format pnm > scan.pnm"
        d = threads.deferToThread(os.system, scan_command)
        d.addCallback(self.process_scan_image)
        d.addErrback(self.scan_error)
        d.addBoth(self.enable_scan_button)

    def process_scan_image(self, _):
        image = Image.open('scan.pnm')
        image.save('scan.png')
        self.image_box.clear_widgets()
        kivy_image = KivyImage(source='scan.png', size_hint=(1, 1))
        self.image_box.add_widget(kivy_image)

    def scan_error(self, failure):
        print("Scanning error: ", failure)

    def enable_scan_button(self, _):
        self.scan_button.disabled = False




if __name__ == '__main__':
    ImageScannerApp().run()