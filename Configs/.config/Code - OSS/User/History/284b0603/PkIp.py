import notify2

notify2.init("Test Bildirimi")
n = notify2.Notification("Test", "Bu bir test bildirimidir.")
n.show()
