import win10toast
notifier=win10toast.ToastNotifier()
def notify(title,message,duration):
	notifier.show_toast(title,message,duration=duration,icon_path="icons/Alert.ico")