import wordpress

title = "Penny - Blue Dress"
image = "/mnt/storage_drive/Andre Art/OC/Hare & Feather/Penny/penny-blue-dress-new.png" 

wplink = wordpress.post(title, image)
print(wplink)
