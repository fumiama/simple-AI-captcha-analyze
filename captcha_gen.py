from PIL import Image, ImageDraw, ImageFont     # 引入绘图模块
import random                                   # 引入随机函数模块
import os, pathlib

class Captcha(object):
	def __init__(self, pic_count, output_dir, font_name, font_size):
		self.pc = pic_count
		self.od = output_dir
		self.fn = font_name
		self.fs = font_size

	def get_random_color(self): return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

	def gen_a_captcha(self):
		# 1.1 定义变量，宽，高，背景颜色
		width = 200
		height = 50
		background_color = (255, 255, 255)
		# 1.2 创建画布对象
		image = Image.new('RGB', (width, height), background_color)
		# 1.3 创建画笔对象
		draw = ImageDraw.Draw(image)
		# 1.4 调用画笔的point()函数绘制噪点
		for i in range(0, 100):
			xy = (random.randrange(0, width), random.randrange(0, height))
			draw.point(xy, fill=self.get_random_color())
		# 1.5 调用画笔的line()函数制造线
		for i in range(0, 10):
			xy_start = (random.randrange(0, width), random.randrange(0, height))
			xy_end = (random.randrange(0, width), random.randrange(0, height))
			draw.line((xy_start, xy_end), fill=self.get_random_color())

		# 2 用draw.text书写文字
		rand_python = ''
		for i in range(4):
			random_number = str(random.randint(0, 9))
			random_lower_letter = chr(random.randint(97, 122))
			random_upper_letter = chr(random.randint(65, 90))
			random_lower_letter2 = chr(random.randint(97, 122))
			random_upper_letter2 = chr(random.randint(65, 90))
			rand_python += random.choice([random_number, random_lower_letter, random_upper_letter, random_lower_letter2, random_upper_letter2])
			color = self.get_random_color()
			text_color = [0, 0, 0]
			for j in range(2):
				if color[j]-background_color[j] <= 30: text_color[j] = (255-color[j]) // 2
				else: text_color[j] = color[j] // 2
			draw.text((i * (width/4) + 10, 2),
					  rand_python[i],
					  tuple(text_color),
					  font=ImageFont.truetype(self.fn, self.fs),
					  align='center')

		# 3 释放画笔
		del draw
		if not self.od.endswith('/'): self.od += '/'
		out_dir = pathlib.Path(self.od)
		if out_dir.is_file(): os.remove(out_dir)
		if not out_dir.exists(): out_dir.mkdir()
		with open(self.od + rand_python + ".png", "wb") as fp: image.save(fp, 'png')

	def gen_captcha(self):
		while self.pc:
			self.gen_a_captcha()
			self.pc -= 1

def cmd():
	import sys
	if len(sys.argv) == 5:
		output_dir = sys.argv[1]
		pic_count = int(sys.argv[2])
		font_name = sys.argv[3]
		font_size = int(sys.argv[4])
		Captcha(pic_count, output_dir, font_name, font_size).gen_captcha()
	else: print("Usage: output_dir pic_count font_name font_size")

if __name__ == '__main__': cmd()