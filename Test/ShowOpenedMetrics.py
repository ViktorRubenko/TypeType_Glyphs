# MenuTitle: Show opened glyphs metrics copy
# -*- coding: utf-8 -*-


from vanilla import *
from AppKit import (
    NSScreen,
    NSScrollView,
    NSView,
    NSTextField,
    NSLayoutConstraint,
    NSLayoutAttributeHeight,
    NSLayoutAttributeWidth,
    NSLayoutAttributeTop,
    NSLayoutAttributeLeading,
    NSLayoutAttributeTrailing,
    NSLayoutAttributeBottom,
    NSLayoutRelationEqual,
    NSColor,
    NSCenterTextAlignment,
)

textbox_width = 40
textbox_gap = 5
textbox_height = 20
glyph_container_width = 100
button_height = 25

metrics_keys = (
    "LSB",
    "RSB",
    "Width",
    "L LF",
    "L RF",
    "L WF",
    "G LF",
    "G RF",
    "G WF",
)


def create_textEdit(text):
    new_textEdit = NSTextField.alloc().init()
    new_textEdit.setTranslatesAutoresizingMaskIntoConstraints_(False)
    constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
        new_textEdit,
        NSLayoutAttributeWidth,
        NSLayoutRelationEqual,
        None,
        0,
        1.0,
        textbox_width,
    )
    if text:
        new_textEdit.setStringValue_(text)
    new_textEdit.addConstraint_(constraint)
    return new_textEdit


def create_textBox(text):
    new_textBox = create_textEdit(text)
    new_textBox.setDrawsBackground_(False)
    new_textBox.setBezeled_(False)
    new_textBox.setEditable_(False)
    return new_textBox


def create_line(color):
    line = NSView.alloc().init()
    line.setBackgroundColor_(color)
    line.setTranslatesAutoresizingMaskIntoConstraints_(False)
    return line


def create_scroll_data_container(data_container):
    scroll_view = NSScrollView.alloc().init()
    scroll_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
    scroll_view.setHasHorizontalScroller_(True)
    scroll_view.setDocumentView_(data_container)

    scroll_view.addConstraint_(
        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            data_container,
            NSLayoutAttributeLeading,
            NSLayoutRelationEqual,
            scroll_view,
            NSLayoutAttributeLeading,
            1.0,
            0,
        )
    )
    scroll_view.addConstraint_(
        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            data_container,
            NSLayoutAttributeTop,
            NSLayoutRelationEqual,
            scroll_view,
            NSLayoutAttributeTop,
            1.0,
            0,
        )
    )
    scroll_view.addConstraint_(
        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            data_container,
            NSLayoutAttributeBottom,
            NSLayoutRelationEqual,
            scroll_view,
            NSLayoutAttributeBottom,
            1.0,
            0,
        )
    )
    # scroll_view.setBackgroundColor_(NSColor.yellowColor())

    return scroll_view


class MetricsWindow:
    def __init__(self):
        self.font = None
        self.data = {}
        self.glyph_order = []
        self.glyph_containers = {}
        self.height = (
            len(metrics_keys) * (textbox_height + 2)
            + textbox_height
            + button_height
            + 5
        )
        self.screen_size = NSScreen.mainScreen().frame().size
        self.w = FloatingWindow(
            (
                self.screen_size.width * 0.6,
                self.height + 15,
            )
        )
        self.w.minSize = (100, self.height + 15)
        self.w.maxSize = (self.screen_size.width * 0.8, self.height + 15)
        self.contentView = self.w._getContentView()

        self.glyph_textBox = create_textBox("Glyph")

        self.hor_line_1 = create_line(NSColor.grayColor())
        self.ver_line_1 = create_line(NSColor.grayColor())
        self.hor_line_2 = create_line(NSColor.grayColor())

        self.data_container = NSView.alloc().init()
        self.data_container.setTranslatesAutoresizingMaskIntoConstraints_(
            False
        )
        self.data_container_width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.data_container,
            NSLayoutAttributeWidth,
            NSLayoutRelationEqual,
            None,
            0,
            1.0,
            len(self.data) * (110),
        )
        self.scroll_data_container = create_scroll_data_container(
            self.data_container
        )
        self.scroll_data_container.addConstraint_(
            self.data_container_width_constraint
        )

        # self.apply_button = NSButton.alloc().init()
        # self.apply_button.setBezelStyle_(NSRegularSquareBezelStyle)
        # self.apply_button.setControlSize_(NSMiniControlSize)
        # self.apply_button.setTitle_("Apply")
        # self.apply_button.setTarget_(self)
        # self.apply_button.setTranslatesAutoresizingMaskIntoConstraints_(False)
        # self.apply_button.setContentCompressionResistancePriority_forOrientation_(
        #     100, NSLayoutConstraintOrientationHorizontal
        # )

        self.w.button = Button(
            (10, -30, 60, 20), "Apply", callback=self.apply_metrics_
        )

        self.contentView.addSubview_(self.glyph_textBox)
        self.contentView.addSubview_(self.hor_line_1)
        self.contentView.addSubview_(self.ver_line_1)
        self.contentView.addSubview_(self.scroll_data_container)
        self.contentView.addSubview_(self.hor_line_2)
        # self.contentView.addSubview_(self.apply_button)

        self._set_constraints()

        textboxes = [create_textBox(metric_key) for metric_key in metrics_keys]
        for index, textbox in enumerate(textboxes):
            self.contentView.addSubview_(textbox)
            if index == 0:
                self.contentView.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        textbox,
                        NSLayoutAttributeTop,
                        NSLayoutRelationEqual,
                        self.hor_line_1,
                        NSLayoutAttributeBottom,
                        1.0,
                        5,
                    )
                )
            else:
                self.contentView.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        textbox,
                        NSLayoutAttributeTop,
                        NSLayoutRelationEqual,
                        textboxes[index - 1],
                        NSLayoutAttributeBottom,
                        1.0,
                        2,
                    )
                )
            self.contentView.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    textbox,
                    NSLayoutAttributeWidth,
                    NSLayoutRelationEqual,
                    None,
                    0,
                    1.0,
                    textbox_width,
                )
            )
            self.contentView.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    textbox,
                    NSLayoutAttributeHeight,
                    NSLayoutRelationEqual,
                    None,
                    0,
                    1.0,
                    textbox_height,
                )
            )
            self.contentView.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    textbox,
                    NSLayoutAttributeLeading,
                    NSLayoutRelationEqual,
                    self.glyph_textBox,
                    NSLayoutAttributeLeading,
                    1.0,
                    0,
                )
            )

        self.reload_glyphs()

        self.w.open()

    def _set_constraints(self):
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.glyph_textBox,
                NSLayoutAttributeTop,
                NSLayoutRelationEqual,
                self.contentView,
                NSLayoutAttributeTop,
                1.0,
                5,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.glyph_textBox,
                NSLayoutAttributeWidth,
                NSLayoutRelationEqual,
                None,
                0,
                1.0,
                textbox_width,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.glyph_textBox,
                NSLayoutAttributeHeight,
                NSLayoutRelationEqual,
                None,
                0,
                1.0,
                textbox_height,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.glyph_textBox,
                NSLayoutAttributeLeading,
                NSLayoutRelationEqual,
                self.contentView,
                NSLayoutAttributeLeading,
                1.0,
                5,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.hor_line_1,
                NSLayoutAttributeTop,
                NSLayoutRelationEqual,
                self.glyph_textBox,
                NSLayoutAttributeBottom,
                1.0,
                0,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.hor_line_1,
                NSLayoutAttributeTrailing,
                NSLayoutRelationEqual,
                self.glyph_textBox,
                NSLayoutAttributeTrailing,
                1.0,
                0,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.hor_line_1,
                NSLayoutAttributeHeight,
                NSLayoutRelationEqual,
                None,
                0,
                1.0,
                1,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.hor_line_1,
                NSLayoutAttributeLeading,
                NSLayoutRelationEqual,
                self.contentView,
                NSLayoutAttributeLeading,
                1.0,
                0,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.ver_line_1,
                NSLayoutAttributeLeading,
                NSLayoutRelationEqual,
                self.hor_line_1,
                NSLayoutAttributeTrailing,
                1.0,
                0,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.ver_line_1,
                NSLayoutAttributeTop,
                NSLayoutRelationEqual,
                self.contentView,
                NSLayoutAttributeTop,
                1.0,
                5,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.ver_line_1,
                NSLayoutAttributeHeight,
                NSLayoutRelationEqual,
                None,
                0,
                1.0,
                self.height - button_height,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.ver_line_1,
                NSLayoutAttributeWidth,
                NSLayoutRelationEqual,
                None,
                0,
                1.0,
                1,
            )
        )

        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.scroll_data_container,
                NSLayoutAttributeLeading,
                NSLayoutRelationEqual,
                self.ver_line_1,
                NSLayoutAttributeTrailing,
                1.0,
                0,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.scroll_data_container,
                NSLayoutAttributeTop,
                NSLayoutRelationEqual,
                self.contentView,
                NSLayoutAttributeTop,
                1.0,
                5,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.scroll_data_container,
                NSLayoutAttributeBottom,
                NSLayoutRelationEqual,
                self.ver_line_1,
                NSLayoutAttributeBottom,
                1.0,
                0,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.scroll_data_container,
                NSLayoutAttributeTrailing,
                NSLayoutRelationEqual,
                self.contentView,
                NSLayoutAttributeTrailing,
                1.0,
                0,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.hor_line_2,
                NSLayoutAttributeTop,
                NSLayoutRelationEqual,
                self.ver_line_1,
                NSLayoutAttributeBottom,
                1.0,
                0,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.hor_line_2,
                NSLayoutAttributeLeading,
                NSLayoutRelationEqual,
                self.contentView,
                NSLayoutAttributeLeading,
                1.0,
                0,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.hor_line_2,
                NSLayoutAttributeTrailing,
                NSLayoutRelationEqual,
                self.contentView,
                NSLayoutAttributeTrailing,
                1.0,
                0,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.hor_line_2,
                NSLayoutAttributeHeight,
                NSLayoutRelationEqual,
                None,
                0,
                1.0,
                1,
            )
        )

        # Button
        # self.contentView.addConstraint_(
        #     NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
        #         self.apply_button,
        #         NSLayoutAttributeHeight,
        #         NSLayoutRelationEqual,
        #         None,
        #         0,
        #         1.0,
        #         button_height,
        #     )
        # )
        # self.contentView.addConstraint_(
        #     NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
        #         self.apply_button,
        #         NSLayoutAttributeLeading,
        #         NSLayoutRelationEqual,
        #         self.contentView,
        #         NSLayoutAttributeLeading,
        #         1.0,
        #         5,
        #     )
        # )
        # self.contentView.addConstraint_(
        #     NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
        #         self.apply_button,
        #         NSLayoutAttributeWidth,
        #         NSLayoutRelationEqual,
        #         None,
        #         0,
        #         1.0,
        #         50,
        #     )
        # )
        # self.contentView.addConstraint_(
        #     NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
        #         self.apply_button,
        #         NSLayoutAttributeBottom,
        #         NSLayoutRelationEqual,
        #         self.contentView,
        #         NSLayoutAttributeBottom,
        #         1.0,
        #         -5,
        #     )
        # )

    def reload_glyphs(self):
        self.data = {}
        self.glyph_order = []
        self.font = Glyphs.font
        current_tab = self.font.currentTab
        if current_tab:
            for layer in current_tab.layers:
                self.glyph_order.append(layer.parent.name)
                self.data[layer.parent.name] = {
                    "RSB": {
                        "value": layer.RSB,
                        "object": None,
                    },
                    "LSB": {
                        "value": layer.LSB,
                        "object": None,
                    },
                    "Width": {
                        "value": layer.width,
                        "object": None,
                    },
                    "L LF": {
                        "value": layer.leftMetricsKey,
                        "object": None,
                    },
                    "L RF": {
                        "value": layer.rightMetricsKey,
                        "object": None,
                    },
                    "L WF": {
                        "value": layer.widthMetricsKey,
                        "object": None,
                    },
                    "G LF": {
                        "value": layer.parent.leftMetricsKey,
                        "object": None,
                    },
                    "G RF": {
                        "value": layer.parent.rightMetricsKey,
                        "object": None,
                    },
                    "G WF": {
                        "value": layer.parent.widthMetricsKey,
                        "object": None,
                    },
                }
        self.reload_glyphs_ui()

    def reload_glyphs_ui(self):
        self.glyph_containers = {}
        self.data_container.setSubviews_([])
        for glyph_name in self.glyph_order:
            metrics = self.data[glyph_name]
            glyph_container = NSView.alloc().init()
            glyph_container.setTranslatesAutoresizingMaskIntoConstraints_(
                False
            )
            # glyph_container.setBackgroundColor_(NSColor.redColor())
            self.glyph_containers[glyph_name] = glyph_container
            self.data_container.addSubview_(glyph_container)

            name_textbox = create_textBox(glyph_name)
            name_textbox.setAlignment_(NSCenterTextAlignment)
            hor_line = create_line(NSColor.grayColor())
            glyph_container.addSubview_(name_textbox)
            glyph_container.addSubview_(hor_line)

            glyph_container.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    name_textbox,
                    NSLayoutAttributeLeading,
                    NSLayoutRelationEqual,
                    glyph_container,
                    NSLayoutAttributeLeading,
                    1.0,
                    0,
                )
            )
            glyph_container.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    name_textbox,
                    NSLayoutAttributeTrailing,
                    NSLayoutRelationEqual,
                    glyph_container,
                    NSLayoutAttributeTrailing,
                    1.0,
                    0,
                )
            )
            glyph_container.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    name_textbox,
                    NSLayoutAttributeTop,
                    NSLayoutRelationEqual,
                    glyph_container,
                    NSLayoutAttributeTop,
                    1.0,
                    0,
                )
            )
            glyph_container.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    name_textbox,
                    NSLayoutAttributeHeight,
                    NSLayoutRelationEqual,
                    None,
                    0,
                    1.0,
                    textbox_height,
                )
            )
            glyph_container.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    hor_line,
                    NSLayoutAttributeHeight,
                    NSLayoutRelationEqual,
                    None,
                    0,
                    1.0,
                    1,
                )
            )
            glyph_container.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    hor_line,
                    NSLayoutAttributeTop,
                    NSLayoutRelationEqual,
                    name_textbox,
                    NSLayoutAttributeBottom,
                    1.0,
                    0,
                )
            )
            glyph_container.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    hor_line,
                    NSLayoutAttributeLeading,
                    NSLayoutRelationEqual,
                    glyph_container,
                    NSLayoutAttributeLeading,
                    1.0,
                    0,
                )
            )
            glyph_container.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    hor_line,
                    NSLayoutAttributeWidth,
                    NSLayoutRelationEqual,
                    glyph_container,
                    NSLayoutAttributeWidth,
                    1.0,
                    1,
                )
            )

            textFields = []
            for metric_key in metrics_keys:
                textField = create_textEdit(metrics[metric_key]["value"])
                self.data[glyph_name][metric_key]["object"] = textField
                textFields.append(textField)

            for index, textfield in enumerate(textFields):
                glyph_container.addSubview_(textfield)
                if index == 0:
                    glyph_container.addConstraint_(
                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                            textfield,
                            NSLayoutAttributeTop,
                            NSLayoutRelationEqual,
                            hor_line,
                            NSLayoutAttributeBottom,
                            1.0,
                            5,
                        )
                    )
                else:
                    glyph_container.addConstraint_(
                        NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                            textfield,
                            NSLayoutAttributeTop,
                            NSLayoutRelationEqual,
                            textFields[index - 1],
                            NSLayoutAttributeBottom,
                            1.0,
                            2,
                        )
                    )
                glyph_container.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        textfield,
                        NSLayoutAttributeTrailing,
                        NSLayoutRelationEqual,
                        glyph_container,
                        NSLayoutAttributeTrailing,
                        1.0,
                        -2,
                    )
                )
                glyph_container.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        textfield,
                        NSLayoutAttributeHeight,
                        NSLayoutRelationEqual,
                        None,
                        0,
                        1.0,
                        textbox_height,
                    )
                )
                glyph_container.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        textfield,
                        NSLayoutAttributeLeading,
                        NSLayoutRelationEqual,
                        glyph_container,
                        NSLayoutAttributeLeading,
                        1.0,
                        2,
                    )
                )

        for index, glyph_name in enumerate(self.glyph_order):
            glyph_container = self.glyph_containers[glyph_name]
            if index == 0:
                self.data_container.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        glyph_container,
                        NSLayoutAttributeLeading,
                        NSLayoutRelationEqual,
                        self.data_container,
                        NSLayoutAttributeLeading,
                        1.0,
                        0,
                    )
                )
            else:
                container_separator = create_line(NSColor.grayColor())
                self.data_container.addSubview_(container_separator)

                self.data_container.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        container_separator,
                        NSLayoutAttributeLeading,
                        NSLayoutRelationEqual,
                        self.glyph_containers[self.glyph_order[index - 1]],
                        NSLayoutAttributeTrailing,
                        1.0,
                        0,
                    )
                )
                self.data_container.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        container_separator,
                        NSLayoutAttributeWidth,
                        NSLayoutRelationEqual,
                        None,
                        0,
                        1.0,
                        1,
                    )
                )
                self.data_container.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        container_separator,
                        NSLayoutAttributeTop,
                        NSLayoutRelationEqual,
                        glyph_container,
                        NSLayoutAttributeTop,
                        1.0,
                        0,
                    )
                )
                self.data_container.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        container_separator,
                        NSLayoutAttributeBottom,
                        NSLayoutRelationEqual,
                        glyph_container,
                        NSLayoutAttributeBottom,
                        1.0,
                        0,
                    )
                )

                self.data_container.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        glyph_container,
                        NSLayoutAttributeLeading,
                        NSLayoutRelationEqual,
                        container_separator,
                        NSLayoutAttributeTrailing,
                        1.0,
                        0,
                    )
                )
            self.data_container.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    glyph_container,
                    NSLayoutAttributeTop,
                    NSLayoutRelationEqual,
                    self.data_container,
                    NSLayoutAttributeTop,
                    1.0,
                    0,
                )
            )
            self.data_container.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    glyph_container,
                    NSLayoutAttributeBottom,
                    NSLayoutRelationEqual,
                    self.data_container,
                    NSLayoutAttributeBottom,
                    1.0,
                    0,
                )
            )
            self.data_container.addConstraint_(
                NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                    glyph_container,
                    NSLayoutAttributeWidth,
                    NSLayoutRelationEqual,
                    None,
                    0,
                    1.0,
                    glyph_container_width,
                )
            )

        width = len(self.data) * (glyph_container_width + 1)
        self.data_container_width_constraint.setConstant_(width)
        self.data_container.invalidateIntrinsicContentSize()

    def apply_metrics_(self, sender):
        current_tab = self.font.currentTab
        if current_tab:
            for layer in current_tab.layers:
                glyph = layer.parent
                if glyph.name not in self.data:
                    continue
                metrics = self.data[glyph.name]

                layer.LSB = self._get_field_value(metrics["LSB"]["object"])
                layer.RSB = self._get_field_value(metrics["RSB"]["object"])
                layer.width = self._get_field_value(metrics["Width"]["object"])

                try:
                    layer.leftMetricsKey = self._get_field_value(
                        metrics["L LF"]["object"]
                    )
                    layer.rightMetricsKey = self._get_field_value(
                        metrics["L RF"]["object"]
                    )
                    layer.widthMetricsKey = self._get_field_value(
                        metrics["L WF"]["object"]
                    )

                    glyph.leftMetricsKey = self._get_field_value(
                        metrics["G LF"]["object"]
                    )
                    glyph.rightMetricsKey = self._get_field_value(
                        metrics["G RF"]["object"]
                    )
                    glyph.widthMetricsKey = self._get_field_value(
                        metrics["G WF"]["object"]
                    )
                except Exception as e:
                    print(glyph.name, "INVALID VALUES")
                    continue

        self.reload_glyphs()

    @staticmethod
    def _size_from_screen():
        size = NSScreen.mainScreen().frame().size
        return int(size.width * 0.55), int(size.height * 0.8)

    @staticmethod
    def _get_field_value(field):
        string_value = field.stringValue()
        return string_value if string_value else None


def main():
    MetricsWindow()


if __name__ == "__main__":
    main()
