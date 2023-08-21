#!/usr/bin/env python
# coding: utf-8
import datetime
import os
import time

from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, Circle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Spacer, SimpleDocTemplate, Table, Paragraph
from reportlab.lib.colors import HexColor
# 注册字体
FONT_FILE_PATH = os.path.join(os.path.dirname(__file__), "msyh.ttf")
IMAGE_PATH = os.path.join(os.path.dirname(__file__), "oasis.png")
pdfmetrics.registerFont(TTFont("msyh", FONT_FILE_PATH))

# 实际为像素
PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]


class Report:
    def __init__(self, job_info, job_res, task_datas, report_path, report_name, language="zh"):
        self.job_info_desc = job_info
        self.job_res_summary = job_res
        self.task_datas_list = task_datas
        self.pie_data = job_res[1:4]
        self.pie_num = job_res[0]
        self.report_path = report_path
        self.report_title = report_name
        self.language = language

    # 绘制页脚信息
    def draw_page_foot_info(self, c: Canvas, doc):
        """绘制页脚"""
        # 设置边框颜色
        c.setStrokeColor(colors.black)
        # 绘制线条
        c.line(30, PAGE_HEIGHT - 800, 560, PAGE_HEIGHT - 800)
        # 绘制页脚文字
        c.setFont("msyh", 8)
        # c.setFillColor(colors.black)
        # c.drawString(30, PAGE_HEIGHT - 810, time.strftime("%Y-%m-%d %H:%M:%S"))
        pageNumber = ("%s" % c.getPageNumber())  # 获取当前的页码
        p = Paragraph(pageNumber)
        p.wrap(1 * cm, 1 * cm)  # 申请一块1cm大小的空间，返回值是实际使用的空间
        p.drawOn(c, PAGE_WIDTH / 2, PAGE_HEIGHT - 820)  # 将页码放在指示坐标处

    # 绘制页眉信息
    def draw_page_header_info(self, c: Canvas, doc):
        """绘制页眉"""
        # 设置边框颜色
        c.setStrokeColor(colors.black)
        # 绘制线条
        c.line(25, PAGE_HEIGHT - 70, 570, PAGE_HEIGHT - 70)
        # # 绘制页眉文字
        c.setFont("msyh", 10)
        c.setFillColor(HexColor("999999"))
        c.drawString(465, PAGE_HEIGHT - 65, "{}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
        self.set_title(c)
        # 使用一个Paragraph Flowable存放图片
        p = Paragraph("<img src='%s' width='%d' height='%d'/>" % (IMAGE_PATH, 65, 15))
        w, h = p.wrap(doc.width, doc.topMargin)
        # p.drawOn(c, doc.leftMargin, doc.topMargin + doc.height - 0.5 * cm)
        p.drawOn(c, 30, PAGE_HEIGHT-30)
        c.setAuthor("OASIS-SIM")
        c.setTitle(self.report_title)
        c.setSubject("OASIS-SIM-TEST-REPORT")

    def set_title(self, c: Canvas):
        # 设置字体大小
        c.setFont("msyh", 24)
        c.setFillColor(colors.black)
        # 绘制居中标题文本
        title = "Report" if self.language == "en" else "测试报告"
        c.drawCentredString(300, PAGE_HEIGHT - 50, title)

    # 绘制作业信息表
    def draw_job_info_table(self, c: Canvas, x, y, data=None):
        """作业信息表"""
        table_header = ["JobName", "Vehicle", "System", "Version", "Start Time", "End Time"]\
            if self.language == "en" else ["作业名称", "测试主车", "受测系统", "软件版本", "测试开始时间", "测试结束时间"]
        datas = []
        for i in list(zip(table_header, data)):
            datas.append(list(i))
        style = [
            ("FONT", (0, 0), (-1, -1), "msyh", 8),  # 单元格字体和大小
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.darkslategray),  # 设置表格内文字颜色
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # 单元格对齐方式
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),  # 单元格对齐方式
            # ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),  # 设置表格框线为grey色，线宽为0.5
            # ('BACKGROUND', (0, 0), (-1, -1), '#d5dae6'),  # 设置第一行背景颜色
        ]
        t = Table(datas, style=style)
        t._argW[0] = 80  # 第一列宽度
        t._argW[1] = 160  # 第二列宽度
        t.wrapOn(c, 0, 0)
        t.drawOn(c, x, y)

    # 绘制作业概览表
    def draw_result_info_table(self, c, x, y, data=None):
        """作业概览表"""
        datas = [["Number", "Passed", "Failed", "Invalid", "TestMileage", "Score", "PassRate"], data] \
            if self.language == "en" else [["场景总数", "通过", "失败", "无效", "总测试里程", "平均得分", "通过率"], data]
        style = [
            ("FONT", (0, 0), (-1, -1), "msyh", 8),  # 单元格字体和大小
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.darkslategray),  # 设置表格内文字颜色
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 单元格对齐方式
            ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),  # 设置表格框线为grey色，线宽为0.5
            ('BACKGROUND', (0, 0), (-1, 0), '#BAD2FF'),  # 设置第一行背景颜色
        ]
        t = Table(datas, style=style, colWidths=68.5, rowHeights=20)
        t.wrapOn(c, 0, 0)
        t.drawOn(c, x, y)

    # 绘制饼图
    def draw_score_pie(self, canvas, x, y, data=None, number=None):
        """绘制测试统计结果饼图"""
        d = Drawing(100, 100)
        # 画大饼图
        pc = Pie()
        pc.width = 100
        pc.height = 100
        # 设置数据
        pc.data = data
        pc.slices.strokeWidth = 0.1
        # 设置颜色
        my_color = [HexColor("#0DB47E"), HexColor("#E6595A"), HexColor("#9D9D9D")]
        pc.slices.strokeColor = colors.transparent
        pc.slices[0].fillColor = my_color[0]
        pc.slices[1].fillColor = my_color[1]
        pc.slices[2].fillColor = my_color[2]
        d.add(pc)
        # 画内圈
        circle = Circle(50, 50, 36)
        circle.fillColor = colors.white
        circle.strokeColor = colors.transparent
        d.add(circle)
        # 图例
        lg = Legend()
        lg.x = 130  # 左上参考点的x坐标
        lg.y = 80  # 左上参考点的y坐标
        lg.dx = 10  # 图例色板宽度
        lg.dy = 10  # 图例色板高度
        lg.deltay = 25  # 图例色块之间的距离
        lg.dxTextSpace = 5  # 色板矩形和文本之间的距离
        lg.fontName = "msyh"
        lg.fontSize = 8
        # lg.colorNamePairs = list(zip(my_color, ["通过  {}".format(data[0]), "失败  {}".format(data[1]), "无效  {}".format(data[2])]))
        title_list = ["Passed", "Failed", "Invalid"] if self.language == "en" else ["通过", "失败", "无效"]
        lg.colorNamePairs = list(zip(my_color, title_list))
        lg.fillColor = colors.darkslategray
        lg.alignment = 'right'
        lg.strokeColor = colors.white
        d.add(lg)
        # 把饼图画到Canvas上
        d.drawOn(canvas, x, y)
        # 图例后的数字
        self.set_pass_num(canvas, data)
        self.set_failure_num(canvas, data)
        self.set_invalid_num(canvas, data)

        # 写字
        canvas.setFont("msyh", 30)
        canvas.setFillColor(colors.grey)
        # todonumber传参写入
        canvas.drawCentredString(x + 50, y + 40, str(number))

    def set_pass_num(self, c: Canvas, data):
        # 设置字体大小
        c.setFont("msyh", 8)
        c.setFillColor(HexColor("#0DB47E"))
        # 指定绘制文本的位置
        c.drawString(514, PAGE_HEIGHT - 133.5, str(data[0]))

    def set_failure_num(self, c: Canvas, data):
        # 设置字体大小
        c.setFont("msyh", 8)
        c.setFillColor(HexColor("#E6595A"))
        # 指定绘制文本的位置
        c.drawString(514, PAGE_HEIGHT - 158.5, str(data[1]))

    def set_invalid_num(self, c: Canvas, data):
        # 设置字体大小
        c.setFont("msyh", 8)
        c.setFillColor(HexColor("#9D9D9D"))
        # 指定绘制文本的位置
        c.drawString(514, PAGE_HEIGHT - 183.5, str(data[2]))

    # 绘制task信息表
    def draw_task_info(self, data=None):
        """task信息表"""
        datas = [["No.", "Name", "SceneID", "SimStatus", "Mileage", "SimTime", "Result", "PassRate"]] if \
            self.language == "en" else [["No.", "场景名称", "场景ID", "运行状态", "测试里程", "仿真时长", "任务结果", "评价通过率"]]
        datas += data
        style = [
            ("FONT", (0, 0), (-1, -1), "msyh", 8),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.darkslategray),  # 设置表格内文字颜色
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            # ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),  # 设置表格框线为grey色，线宽为0.5
            ('BACKGROUND', (0, 0), (-1, 0), '#BAD2FF'),  # 设置第一行背景颜色
        ]
        t = Table(datas, style=style, colWidths=[30, 190, 42, 42, 42, 42, 42, 52], rowHeights=20)
        return t

    def draw_little_title(self, c: Canvas, x, y, text=""):
        """绘制左右边小标题"""
        c.saveState()
        # 设置填充色
        c.setFillColor(colors.black)
        # 设置字体大小
        c.setFont("msyh", 12)
        # 绘制小标题文本
        c.drawCentredString(x, y, text)

    def my_first_page(self, c: Canvas, doc):
        c.saveState()
        # 设置填充色
        c.setFillColor(colors.black)
        # # 设置字体大小
        # c.setFont("msyh", 30)
        # # 绘制居中标题文本
        # c.drawCentredString(300, PAGE_HEIGHT - 60, "OASIS Sim测试报告")
        # 绘制小标题
        self.draw_little_title(c, x=108 if self.language == "en" else 80, y=PAGE_HEIGHT - 95, text="Basic Information" if self.language == "en" else "基本信息")
        self.draw_little_title(c, x=368 if self.language == "en" else 340, y=PAGE_HEIGHT - 95, text="Simulation Results" if self.language == "en" else"结果统计")
        # 绘制作业信息表格
        self.draw_job_info_table(c, 55, PAGE_HEIGHT - 200, data=self.job_info_desc)
        # 绘制结果统计饼图
        self.draw_score_pie(c, 340, PAGE_HEIGHT - 205, data=self.pie_data, number=self.pie_num)
        self.draw_little_title(c, x=80, y=PAGE_HEIGHT - 225, text="Results" if self.language == "en" else "结果汇总")
        # 绘制结果概览表[100, 71, 20, 9, "{}km".format(0.8), 85, "{:.2%}".format(71/100)]
        self.draw_result_info_table(c, 58, PAGE_HEIGHT - 275, data=self.job_res_summary)
        # 绘制task详情小标题
        self.draw_little_title(c, x=80, y=PAGE_HEIGHT - 300, text="Details" if self.language == "en" else "测试详情")
        # 绘制页眉
        self.draw_page_header_info(c, doc)
        # 绘制页脚
        self.draw_page_foot_info(c, doc)
        c.restoreState()

    def my_later_pages(self, c: Canvas, doc):
        c.saveState()
        # 绘制页眉页脚
        self.draw_page_header_info(c, doc)
        self.draw_page_foot_info(c, doc)
        c.restoreState()

    def create_file(self):
        # 创建文档
        doc = SimpleDocTemplate(self.report_path, pagesize=A4)
        content = list()
        # 绘制段落
        content.append(Spacer(1, 8.2 * cm))
        # 绘制task详情表
        content.append(self.draw_task_info(data=self.task_datas_list))
        doc.build(content, onFirstPage=self.my_first_page, onLaterPages=self.my_later_pages)
        return self.report_path


if __name__ == '__main__':
    # only test execute
    job_infos = ["oasis-job-1", "全闭环车辆", "oasis-driver", "oasis 1.5.0", "2022-12-07 14:54:07", "2022-12-07 14:56:07"]
    job_ress = [100, 71, 20, 9, "{}km".format(0.8), 85, "{:.2%}".format(71/100)]
    task_data = [["1", "TurnLeft(I)_V1(OL)GoStraight_V2(OL)GoStraight", "8", "完成", "20m", "00:40:00", "失败", "8/10"] for i in range(80)]
    # report_out_path_ = os.path.join(os.path.dirname(__file__), "/output.pdf")
    report_out_path_ = "/home/jsc-computer/Code/oasis-code/server/apps/job/out_put.pdf"
    report_title = "oasis-sim-test-report"
    path = Report(job_infos, job_ress, task_data, report_out_path_, report_title, language='zh').create_file()
    print(path)
