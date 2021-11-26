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
    NSRectFill,
    NSCenterTextAlignment,
)

textbox_width = 40
textbox_gap = 5
textbox_height = 20
glyph_container_width = 100

metrics_keys = ("LSB", "RSB", "Width", "LF", "RF", "WF", "GLF", "GRF", "GWF")


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
    scroll_view.setBackgroundColor_(NSColor.yellowColor())

    return scroll_view


class MetricsWindow:
    def __init__(self):
        self.data = {}
        self.glyph_containers = []
        self.height = (
            len(metrics_keys) * (textbox_height + 2) + textbox_height + 15
        )
        self.screen_size = NSScreen.mainScreen().frame().size
        self.w = Window(
            (
                self.screen_size.width * 0.8,
                self.height,
            )
        )
        self.contentView = self.w._getContentView()

        self.glyph_textBox = create_textBox("Glyph")

        self.hor_line_1 = create_line(NSColor.grayColor())
        self.ver_line_1 = create_line(NSColor.grayColor())

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
        print(self.data_container_width_constraint)

        self.contentView.addSubview_(self.glyph_textBox)
        self.contentView.addSubview_(self.hor_line_1)
        self.contentView.addSubview_(self.ver_line_1)
        self.contentView.addSubview_(self.scroll_data_container)

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
                        NSLayoutAttributeTop,
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
                0,
            )
        )
        self.contentView.addConstraint_(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.ver_line_1,
                NSLayoutAttributeBottom,
                NSLayoutRelationEqual,
                self.contentView,
                NSLayoutAttributeBottom,
                1.0,
                0,
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
                5,
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
                self.contentView,
                NSLayoutAttributeBottom,
                1.0,
                -5,
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
                -5,
            )
        )

    def reload_glyphs(self):
        self.data = {}
        font = Glyphs.font
        current_tab = font.currentTab
        if current_tab:
            for layer in current_tab.layers:
                self.data[layer.parent.name] = {
                    "RSB": layer.RSB,
                    "LSB": layer.LSB,
                    "Width": layer.width,
                    "LF": layer.leftMetricsKey,
                    "RF": layer.rightMetricsKey,
                    "WF": layer.widthMetricsKey,
                    "GLF": layer.parent.leftMetricsKey,
                    "GRF": layer.parent.rightMetricsKey,
                    "GWF": layer.parent.widthMetricsKey,
                }
        print(self.data)
        self.reload_glyphs_ui()

    def reload_glyphs_ui(self):
        self.glyph_containers = []
        self.data_container.setSubviews_([])
        for glyph_name, metrics in self.data.items():
            glyph_container = NSView.alloc().init()
            glyph_container.setTranslatesAutoresizingMaskIntoConstraints_(
                False
            )
            glyph_container.setBackgroundColor_(NSColor.redColor())
            self.glyph_containers.append(glyph_container)
            self.data_container.addSubview_(glyph_container)

            name_textbox = create_textBox(glyph_name)
            name_textbox.setAlignment_(NSCenterTextAlignment)
            glyph_container.addSubview_(name_textbox)

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

        for index, glyph_container in enumerate(self.glyph_containers):
            if index == 0:
                self.contentView.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        glyph_container,
                        NSLayoutAttributeLeading,
                        NSLayoutRelationEqual,
                        self.data_container,
                        NSLayoutAttributeLeading,
                        1.0,
                        5,
                    )
                )
            else:
                self.contentView.addConstraint_(
                    NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                        glyph_container,
                        NSLayoutAttributeLeading,
                        NSLayoutRelationEqual,
                        self.glyph_containers[index - 1],
                        NSLayoutAttributeTrailing,
                        1.0,
                        5,
                    )
                )
            self.contentView.addConstraint_(
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
            self.contentView.addConstraint_(
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
            self.contentView.addConstraint_(
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

        width = len(self.data) * (glyph_container_width + 5) + 5
        self.data_container_width_constraint.setConstant_(width)
        self.data_container.invalidateIntrinsicContentSize()

    @staticmethod
    def _size_from_screen():
        size = NSScreen.mainScreen().frame().size
        return int(size.width * 0.55), int(size.height * 0.8)


def main():
    MetricsWindow()


if __name__ == "__main__":
    main()
