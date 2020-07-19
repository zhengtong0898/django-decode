import wx
import wx.grid
import typing
from pubsub import pub


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="A Simple Grid", size=(900, 400))
        self.panel = wx.Panel(self)
        pub.subscribe(self.grid_rerender, "grid_rerender")                  # grid_update.connect(self.grid_rerender)

        # 初始化数据
        # [
        #  ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
        #  ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        #  ['21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
        # ]
        items = [[str(row*10 + col + 1).zfill(2) for col in range(10)] for row in range(3)]
        rows, cols = len(items), 10
        self.grid = wx.grid.Grid(self.panel)
        self.grid.CreateGrid(rows, cols)
        wx.CallAfter(pub.sendMessage, "grid_rerender", **{"items": items})                      # grid_update.send()

        # 软件窗体布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)

        # 模拟一些数据, 三秒后重新渲染表格
        # [
        #  ['081', '082', '083', '084', '085', '086', '087', '088', '089', '090']
        #  ['091', '092', '093', '094', '095', '096', '097', '098', '099', '100']
        #  ['101', '102', '103', '104', '105', '106', '107', '108', '109', '110']
        #  ['111', '112', '113', '114', '115', '116', '117', '118', '119', '120']
        #  ['121', '122', '123', '124', '125', '126', '127', '128', '129', '130']
        #  ['131', '132', '133', '134', '135', '136', '137', '138', '139', '140']
        #  ['141', '142', '143', '144', '145', '146', '147', '148', '149', '150']
        #  ['151', '152', '153', '154', '155', '156', '157', '158', '159', '160']
        # ]
        items = [[str(row * 10 + col + 1).zfill(3) for col in range(10)] for row in range(8, 16)]
        wx.CallLater(3000, pub.sendMessage, "grid_rerender", **{"items": items})                # grid_update.send()

    def grid_rerender(self, items: typing.List):
        if not getattr(self, "grid"): raise RuntimeError("grid is not initialize")
        all_rows = self.grid.GetNumberRows()
        self.grid.DeleteRows(0, all_rows)
        self.grid.AppendRows(len(items))
        for row, item in enumerate(items):
            for col, value in enumerate(item):
                self.grid.SetCellValue(row, col, value)


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
