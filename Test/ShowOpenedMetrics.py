# MenuTitle: Show opened glyphs metrics
# -*- coding: utf-8 -*-


from vanilla import *
from AppKit import (
    NSScreen,
    NSView,
    NSTextField,
    NSMiniControlSize,
    NSShadowlessSquareBezelStyle,
    NSCircularBezelStyle,
    NSLayoutConstraint,
    NSLayoutAttributeHeight,
    NSLayoutAttributeWidth,
    NSLayoutAttributeTop,
    NSLayoutAttributeLeading,
    NSLayoutAttributeTrailing,
    NSLayoutAttributeBottom,
    NSLayoutRelationEqual,
    NSLineBreakByTruncatingTail,
    NSLayoutConstraintOrientationHorizontal,
)

textbox_width = 100
textbox_gap = 15
textbox_height = 30

metrics_keys = ("LSB", "RSB", "Width", "LF", "RF", "WF")


def new_textbox(frame, text):
    new_textbox = NSTextField.alloc().initWithFrame_(frame)
    new_textbox.setTranslatesAutoresizingMaskIntoConstraints_(False)
    constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
        new_textbox,
        NSLayoutAttributeWidth,
        NSLayoutRelationEqual,
        None,
        0,
        1.0,
        textbox_width,
    )
    if text:
        new_textbox.setStringValue_(text)
    new_textbox.addConstraint_(constraint)
    return new_textbox


class MetricsWindow:
    def __init__(self):
        self.data = {}
        self.screen_size = NSScreen.mainScreen().frame().size
        self.w = Window((self.screen_size.width * 0.8, 180))
        self.view = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 180, 160))
        self.view.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self.widthConstraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.view,
            NSLayoutAttributeWidth,
            NSLayoutRelationEqual,
            None,
            0,
            1.0,
            0,
        )
        self.view.addConstraint_(self.widthConstraint)

        self.textEdit_container = NSView.alloc().initWithFrame_(
            NSMakeRect(0, 0, 180, 160)
        )
        self.textEdit_container.setTranslatesAutoresizingMaskIntoConstraints_(
            False
        )

        self.view.addSubview_(self.textEdit_container)
        constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.view,
            NSLayoutAttributeLeading,
            NSLayoutRelationEqual,
            self.textEdit_container,
            NSLayoutAttributeLeading,
            1.0,
            0,
        )
        self.view.addConstraint_(constraint)

        constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.view,
            NSLayoutAttributeTrailing,
            NSLayoutRelationEqual,
            self.textEdit_container,
            NSLayoutAttributeTrailing,
            1.0,
            15,
        )
        self.view.addConstraint_(constraint)

        self.setup_textedits()

        self.w.scrollView = ScrollView((10, 10, -10, -10), self.view)

        self.w.center()
        self.w.open()

    def setup_textedits(self):
        self.load_data()
        width_start = 5
        height_start = 0
        quantity = len(self.data)
        width = quantity * (textbox_width + textbox_gap)
        print(self.widthConstraint)
        self.widthConstraint.setConstant_(width)
        print(self.widthConstraint)
        if quantity == 0:
            return
        self.textEdit_container.setSubviews_([])
        for glyph_name, metrics in self.data.items():
            height = 160
            text_edit = new_textbox(
                NSMakeRect(
                    width_start,
                    height - height_start - textbox_height,
                    textbox_width,
                    height,
                ),
                glyph_name,
            )
            self.textEdit_container.addSubview_(text_edit)
            height -= textbox_height - 10
            for metric_key in metrics_keys:
                text_edit = new_textbox(
                    NSMakeRect(
                        width_start,
                        height - height_start - textbox_height,
                        textbox_width,
                        height,
                    ),
                    metrics[metric_key],
                )
                self.textEdit_container.addSubview_(text_edit)
                height -= textbox_height - 10
            width_start += textbox_width + textbox_gap
        self.view.invalidateIntrinsicContentSize()

    def load_data(self):
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
                }
        print(self.data)

    @staticmethod
    def _size_from_screen():
        size = NSScreen.mainScreen().frame().size
        return int(size.width * 0.55), int(size.height * 0.8)


def main():
    MetricsWindow()


if __name__ == "__main__":
    main()
