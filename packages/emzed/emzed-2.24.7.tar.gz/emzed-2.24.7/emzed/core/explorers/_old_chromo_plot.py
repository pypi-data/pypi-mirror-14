class ChromatogramPlot(object):  # CurvePlot):

    # as we use this class for patching by setting this class as super class of a given
    # CurvePlot instance, we do not call __init__, instead we set defaults here:

    image_plot = None

    def label_info(self, x, y):
        return "label_info"

    def on_plot(self, x, y):
        return (x, y)

    @protect_signal_handler
    def do_move_marker(self, event):
        pos = event.pos()
        rt = self.invTransform(self.xBottom, pos.x())
        if self.image_plot:
            self.image_plot.set_rt(rt)
        self.set_marker_axes()
        self.cross_marker.setZ(self.get_max_z() + 1)
        self.cross_marker.setVisible(True)
        self.cross_marker.move_local_point_to(0, pos)
        self.replot()

    def set_rt(self, rt):
        self.cross_marker.setValue(rt, self.cross_marker.yValue())
        self.replot()

    def do_zoom_view(self, dx, dy, lock_aspect_ratio=False):
        """ disables zoom """
        pass

    def do_pan_view(self, dx, dy):
        """ disables panning """
        pass

    def plot_chromatograms(self, rts, chroma, rts2, chroma2):
        self.del_all_items()
        if rts2 is None:
            curve = make.curve(rts, chroma, linewidth=1.5, color="#666666")
            curve.__class__ = ModifiedCurveItem
            self.add_item(curve)
        else:
            curve = make.curve(rts, chroma, linewidth=1.5, color="#aaaa00")
            curve.__class__ = ModifiedCurveItem
            self.add_item(curve)
            curve = make.curve(rts2, chroma2, linewidth=1.5, color="#0000aa")
            curve.__class__ = ModifiedCurveItem
            self.add_item(curve)

        def mmin(seq, default=1.0):
            return min(seq) if len(seq) else default

        def mmax(seq, default=1.0):
            return max(seq) if len(seq) else default

        self.add_item(self.rt_label)
        rtmin = mmin(rts, default=0.0)
        rtmax = mmax(rts)
        maxchroma = mmax(chroma)
        if rts2 is not None:
            rtmin = min(rtmin, mmin(rts2, rtmin))
            rtmax = max(rtmax, mmax(rts2, rtmax))
            maxchroma = max(maxchroma, mmax(chroma2, maxchroma))
        self.set_plot_limits(rtmin, rtmax, 0, maxchroma)
        self.updateAxes()
        self.replot()


class ChromatogramPlotter(object):

    def __init__(self, image_plot):
        self.widget = create_chromatogram_widget(image_plot)
        set_x_axis_scale_draw(self.widget)
        set_y_axis_scale_draw(self.widget)

    def plot(self, rts, chroma, rts2=None, chroma2=None):
        self.widget.plot.plot_chromatograms(rts, chroma, rts2, chroma2)
        self.widget.plot.updateAxes()



def create_chromatogram_widget(image_plot):
    widget = CurveWidget(ylabel="I")
    t = widget.add_tool(SelectTool)
    widget.set_default_tool(t)
    t.activate()

    plot = widget.plot
    plot.__class__ = ChromatogramPlot
    plot.image_plot = image_plot
    image_plot.chromatogram_plot = plot

    plot.set_antialiasing(True)
    plot.cross_marker.setZ(plot.get_max_z() + 1)
    plot.cross_marker.setVisible(True)
    plot.canvas_pointer = True  # x-cross marker on

    cursor_info = RtCursorInfo()
    label = make.info_label("TR", [cursor_info], title="None")
    label.labelparam.label = ""
    label.labelparam.font.size = 12
    label.setVisible(1)
    label.labelparam.update_label(label)
    plot.rt_label = label

    # we hack label_cb for updating legend:
    def label_cb(rt, mz):
        # passing None here arives as np.nan if you call get_rect later, so we use
        # np.nan here:
        cursor_info.set_rt(rt)
        return ""
    cross_marker = plot.cross_marker
    cross_marker.label_cb = label_cb
    params = {
        "marker/cross/line/color": "#cccccc",
        "marker/cross/line/width": 1.5,
        "marker/cross/line/style": "DashLine",
        "marker/cross/line/alpha": 0.4,
        "marker/cross/markerstyle": "VLine",
        "marker/cross/symbol/marker": "NoSymbol",
    }
    CONF.update_defaults(dict(plot=params))
    cross_marker.markerparam.read_config(CONF, "plot", "marker/cross")
    cross_marker.markerparam.update_marker(cross_marker)
    return widget

