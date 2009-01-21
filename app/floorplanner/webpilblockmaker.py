import Image, ImageDraw, ImageColor

class BlockMaker:
    def __init__(self, width, height, texture, rooms,
            dimensions=[],description=[], name = 'testi'):

        self.dimensions=dimensions
        self.description=description

        self.width = width
        self.height = height
        self.rooms = rooms

        if texture:
            self.floorplan = self.draw_pil_texture()
        else:
            self.floorplan = self.draw_pil()

        self.floorplan.save(name, 'JPEG')

#-------------------------------------------#
    def get_pil_room(self, room_type, x, y):
        '''
        Return a bitmap corresponding to the room type.
        '''
        tmp_room = self.rooms[room_type].copy()
        tmp_room = tmp_room.resize((int(x), int(y)), Image.BICUBIC)
        return tmp_room

#-------------------------------------------#
    def get_pil_roomDesc(self):
        coordinates = []
        roomsizes = []

        for i in xrange(0, len(self.dimensions)):
            coordinates.append(float(self.dimensions[i][0]))
            coordinates.append(float(self.dimensions[i][1]))
            roomsizes.append(float(self.dimensions[i][2])-float(self.dimensions[i][0]))
            roomsizes.append(float(self.dimensions[i][3])-float(self.dimensions[i][1]))

        return coordinates, roomsizes

#-------------------------------------------#
    def draw_pil(self):
        '''
            Draw the floorplan rooms using a different color for each room.
        '''
        coordinates, roomsizes = self.get_pil_roomDesc()
        img = Image.new('RGBA', (self.width,self.height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        #color_scheme = [ 'rgb(130,132,153)', 'rgb(20,37,204)', 'rgb(0,157,255)', 'rgb(255,187,134)', 'rgb(204,74,20)' ]
        #color_scheme = [ 'rgb(243,134,140)', 'rgb(112,195,177)', 'rgb(144,177,72)', 'rgb(91,174,102)', 'rgb(125,156,159)' ]
        #color_scheme = [ 'rgb(255,249,237)', 'rgb(189,182,138)', 'rgb(224,125,18)', 'rgb(211,230,240)', 'rgb(227,227,212)' ]
        color_scheme = [ 'rgb(227,231,213)', 'rgb(31, 101, 133)', 'rgb(233,255,112)', 'rgb(158,32,73)', 'rgb(169,176,169)' ]

        i = 0
        outline_color = 'black'
        for j in xrange(0, len(self.dimensions)):
            desc = self.description[j]
            if desc == 'S':
                #color_fill = 'white'
                color_fill = color_scheme[0]

            # RST - Restroom, BTH - Bathroom : FIREBRICK
            elif desc == 'RST' or desc == 'BTH':
                #color_fill = 'firebrick'
                color_fill = color_scheme[1]

            # KTH - Kitchen, DIN - Dining Room : GREEN
            elif desc == 'KTH' or desc == 'DIN':
                #color_fill = 'green'
                color_fill = color_scheme[2]

            # LIV - Living Room, LBK - Living/Bed/Kitchen Combo, LKT - Living/Kitchen Combo : RED
            elif desc == 'LIV' or desc == 'LBK' or desc == 'LKT':
                #color_fill = 'red'
                color_fill = color_scheme[3]

            # BED - Bed Room : YELLOW
            elif desc == 'MBR' or desc == 'GBR' or desc == 'BED': 
                #color_fill = 'yellow'
                color_fill = color_scheme[4]

            # Other rooms
            else:
                #color_fill = 'gray'
                color_fill = color_scheme[5]

            draw.rectangle([coordinates[i], coordinates[i+1], coordinates[i]+roomsizes[i], coordinates[i+1]+roomsizes[i+1]],
                    fill = color_fill, outline = outline_color)
            draw.text((coordinates[i], coordinates[i+1]), desc, outline_color)
            i += 2

        return img

#-------------------------------------------#
    def draw_pil_texture(self):
        '''
        Draw the floorplan rooms using textures.
        '''
        coordinates, roomsizes = self.get_pil_roomDesc()
        img = Image.new('RGBA', (self.width,self.height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        i = 0
        outline_color = 'black'
        for j in xrange(0, len(self.dimensions)):

            x1, y1 = int(coordinates[i]), int(coordinates[i+1])
            x2, y2 = int(coordinates[i]+roomsizes[i]), int(coordinates[i+1]+roomsizes[i+1])

            if self.description[j] == 'S':
                color_fill = 'white'
                draw.rectangle([x1, y1, x2, y2],
                        fill = color_fill, outline = outline_color)
            # RST - Restroom, BTH - Bathroom : FIREBRICK
            elif self.description[j] == 'RST' or self.description[j] == 'BTH':
                room = self.get_pil_room('bath', roomsizes[i], roomsizes[i+1])
                img.paste(room, (x1, y1))

            # KTH - Kitchen, DIN - Dining Room : GREEN
            elif self.description[j] == 'KTH' or self.description[j] == 'DIN':
                room = self.get_pil_room('kitchen', roomsizes[i], roomsizes[i+1])
                img.paste(room, (x1, y1))

            # LIV - Living Room, LBK - Living/Bed/Kitchen Combo, LKT - Living/Kitchen Combo : RED
            elif self.description[j] == 'LIV' or self.description[j] == 'LBK' or self.description[j] == 'LKT':
                room = self.get_pil_room('livingroom', roomsizes[i], roomsizes[i+1])
                img.paste(room, (x1, y1))

            # BED - Bed Room : YELLOW
            elif self.description[j] == 'MBR' or self.description[j] == 'GBR' or self.description[j] == 'BED': 
                room = self.get_pil_room('bedroom', roomsizes[i], roomsizes[i+1])
                img.paste(room, (x1, y1))

            # Other rooms
            else:
                color_fill = 'gray'
                draw.rectangle([x1, y1, x2, y2],
                        fill = color_fill, outline = outline_color)
            i += 2

        w, h = self.width, self.height
        draw.line([0,0, w,0, w,h, 0,h, 0,0], fill = 'black', width=4)

        return img

#-------------------------------------------#
