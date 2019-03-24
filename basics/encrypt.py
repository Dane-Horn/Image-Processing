from image import Image

apple = Image(filename='source_images/apple.pnm').weighted_avg_gray()
apple = apple.threshed(100)
apple.write_to_file('results/apple_threshed')
secret1, secret2 = apple.cryptFiend()
secret1.write_to_file('results/apple_secret1')
secret2.write_to_file('results/apple_secret2')
reconstructed = secret1.mask_and(secret2)
reconstructed.write_to_file('results/apple_answer')
