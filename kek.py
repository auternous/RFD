import wx

app = wx.App(False)


def get_k(width=wx.GetDisplaySize()[0], height=wx.GetDisplaySize()[1]):
    MINIMUM_SIZE = (800, 600)
    k_width = width // MINIMUM_SIZE[0]
    k_height = height // MINIMUM_SIZE[1]
    return (k_width, k_height)
