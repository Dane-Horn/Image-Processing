from image import Image
apple = Image(filename='source_images/apple.pnm')
new_apple = apple.hideMessage('hello world')
new_apple.write_to_file('results/hidden_apple')
print(apple.getMessage(new_apple))
