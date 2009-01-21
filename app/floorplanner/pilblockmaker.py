import wx
import gui.feedbackpanel as feedbackpanel
from iga.gacommon import gaParams
import Image, ImageDraw, ImageColor

class BlockMaker(feedbackpanel.FeedbackPanel):
    def __init__(self,parent,ID=-1,dimensions=[],description=[],pos=wx.DefaultPosition,size=(220,260)):
        feedbackpanel.FeedbackPanel.__init__(self,parent,ID,size)

        self.parent = parent
        self.SetBackgroundColour(wx.WHITE)
        self.dimensions=dimensions
        self.description=description
        self.SetMinSize(size)

        appVar = gaParams.getVar('application')
        self.width = appVar['plotSizeX']
        self.height = appVar['plotSizeY']

        rooms = {}
        rooms['bath'] = Image.open('app/floorplanner/bath.png')
        rooms['bedroom'] = Image.open('app/floorplanner/bedroom.png')
        rooms['kitchen'] = Image.open('app/floorplanner/kitchen.png')
        rooms['livingroom'] = Image.open('app/floorplanner/livingroom.png')
        self.rooms = rooms
        self.xoffset = 25.0
        self.yoffset = 40.0

        if appVar.has_key('texture') and appVar['texture']:
            self.floorplan = self.draw_pil_texture()
        else:
            self.floorplan = self.draw_pil()

        self.Bind(wx.EVT_PAINT, self.draw)

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
    def draw(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.floorplan, self.xoffset, self.yoffset)

#-------------------------------------------#
    def draw_pil(self):
        '''
            Draw the floorplan rooms using a different color for each room.
        '''
        coordinates, roomsizes = self.get_pil_roomDesc()
        img = Image.new('RGBA', (self.width,self.height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        i = 0
        outline_color = 'black'
        for j in xrange(0, len(self.dimensions)):
            if self.description[j] == 'S':
                color_fill = 'white'

            # RST - Restroom, BTH - Bathroom : FIREBRICK
            elif self.description[j] == 'RST' or self.description[j] == 'BTH':
                color_fill = 'firebrick'

            # KTH - Kitchen, DIN - Dining Room : GREEN
            elif self.description[j] == 'KTH' or self.description[j] == 'DIN':
                color_fill = 'green'

            # LIV - Living Room, LBK - Living/Bed/Kitchen Combo, LKT - Living/Kitchen Combo : RED
            elif self.description[j] == 'LIV' or self.description[j] == 'LBK' or self.description[j] == 'LKT':
                color_fill = 'red'

            # BED - Bed Room : YELLOW
            elif self.description[j] == 'MBR' or self.description[j] == 'GBR' or self.description[j] == 'BED': 
                color_fill = 'yellow'

            # Other rooms
            else:
                color_fill = 'gray'

            draw.rectangle([coordinates[i], coordinates[i+1], coordinates[i]+roomsizes[i], coordinates[i+1]+roomsizes[i+1]],
                    fill = color_fill, outline = outline_color)
            i += 2

        return self.pil_to_bitmap(img)

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
            if self.description[j] == 'S':
                color_fill = 'white'
                draw.rectangle([coordinates[i], coordinates[i+1], coordinates[i]+roomsizes[i], coordinates[i+1]+roomsizes[i+1]],
                        fill = color_fill, outline = outline_color)
            # RST - Restroom, BTH - Bathroom : FIREBRICK
            elif self.description[j] == 'RST' or self.description[j] == 'BTH':
                room = self.get_pil_room('bath', roomsizes[i], roomsizes[i+1])
                img.paste(room, (coordinates[i], coordinates[i+1]))

            # KTH - Kitchen, DIN - Dining Room : GREEN
            elif self.description[j] == 'KTH' or self.description[j] == 'DIN':
                room = self.get_pil_room('kitchen', roomsizes[i], roomsizes[i+1])
                img.paste(room, (coordinates[i], coordinates[i+1]))

            # LIV - Living Room, LBK - Living/Bed/Kitchen Combo, LKT - Living/Kitchen Combo : RED
            elif self.description[j] == 'LIV' or self.description[j] == 'LBK' or self.description[j] == 'LKT':
                room = self.get_pil_room('livingroom', roomsizes[i], roomsizes[i+1])
                img.paste(room, (coordinates[i], coordinates[i+1]))

            # BED - Bed Room : YELLOW
            elif self.description[j] == 'MBR' or self.description[j] == 'GBR' or self.description[j] == 'BED': 
                room = self.get_pil_room('bedroom', roomsizes[i], roomsizes[i+1])
                img.paste(room, (coordinates[i], coordinates[i+1]))

            # Other rooms
            else:
                color_fill = 'gray'
                draw.rectangle([coordinates[i], coordinates[i+1], coordinates[i]+roomsizes[i], coordinates[i+1]+roomsizes[i+1]],
                        fill = color_fill, outline = outline_color)
            i += 2

        w, h = self.width, self.height
        draw.line([0,0, w,0, w,h, 0,h, 0,0], fill = 'black', width=4)

        return self.pil_to_bitmap(img)

#-------------------------------------------#
    def pil_to_bitmap(self, pil_img):

        image = apply(wx.EmptyImage, pil_img.size)
        image.SetData(pil_img.convert('RGB').tostring())
        image.SetAlphaData(pil_img.convert('RGBA').tostring()[3::4])
        return image.ConvertToBitmap()

#-------------------------------------------#
