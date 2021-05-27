from PIL import Image, ImageFont, ImageDraw
import numpy as np
import csv
import os, tkinter, tkinter.filedialog, tkinter.messagebox, tkinter.filedialog
import qrcode


def main():
    systemName = '団体チケット一括発券システム'

    # 【原画選択】
    # ファイル選択ダイアログの表示
    root = tkinter.Tk()
    root.withdraw()
    # ファイルタイプを制限　fTyp = [("","*")]
    fTyp = [("", "*.png")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo(systemName, '画像テンプレートを選択してください！')
    img_src = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)

    # 【CSV選択】
    # ファイル選択ダイアログの表示
    root = tkinter.Tk()
    root.withdraw()
    # ファイルタイプを制限　fTyp = [("","*")]
    fTyp = [("", "*.csv")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo(systemName, 'CSVを選択してください！')
    csv_src = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)

    # 【保存先選択】
    # ファイル選択ダイアログの表示
    root = tkinter.Tk()
    root.withdraw()
    # ファイルタイプを制限　fTyp = [("","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo(systemName, '保存先を選択してください！')
    save_src = tkinter.filedialog.askdirectory(initialdir = iDir)

    # CSV -> List
    with open(csv_src, encoding='utf8') as f:  # siftJis? ->encoding='cp932'
        reader = csv.reader(f)
        l = [row for row in reader]
    # List総数
    total = len(l)
    cnt = 0

    # フォント指定
    font_path = "./font/ヒラギノ丸ゴ ProN W4.ttc"
    font_size_name = 44
    font_size_ticketNo = 44

    # 保存サイズを指定
    img_save_size = 1227, 1751

    # 【テキスト入れ】
    # row[0] => チケットNo
    # row[1] => ゲストネーム

    for row in l:
        # 処理状況出力
        cnt += 1
        print(str(round(cnt/total*100, 2)) + "%(" + str(cnt) + "/" + str(total) + ") " + row[0] + row[1] + " 様")

        # img = Image.fromarray(img)  # cv2(NumPy)型の画像をPIL型に変換
        img = Image.open(img_src)
        img.thumbnail(img_save_size)
        draw = ImageDraw.Draw(img)  # 描画用のDraw関数を用意

        # PILでフォントを定義
        font_name = ImageFont.truetype(font_path, font_size_name)
        font_ticketNo = ImageFont.truetype(font_path, font_size_ticketNo)

        # ピクセルサイズを取得
        w_name, h_name = draw.textsize(row[1]+" 様", font_name)
        w_ticketNo, h_ticketNo = draw.textsize(row[0], font_ticketNo)

        # テキストを描画（位置、文章、フォント、文字色(BGR+α)を指定）
        # draw.text((614-w_name/2, 1190-h_name/2), row[1], font=font_name, fill=(0, 0, 0, 0))
        # draw.text((614-w_ticketNo/2, 1283-h_ticketNo/2), row[0], font=font_ticketNo, fill=(0, 0, 0, 0))
        draw.text((614-w_name/2, 1190-h_name/2), row[1]+" 様", font=font_name, fill=(0, 0, 0))
        draw.text((614-w_ticketNo/2, 1283-h_ticketNo/2), row[0], font=font_ticketNo, fill=(0, 0, 0))


        # QRを作成
        qr = qrcode.QRCode(
            version=12,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=7,
            border=0,
        )
        qr.add_data('https://www.wixevents.com/check-in/'+row[0]+',f1ac71ba-38121526')
        qr.make()
        img_qr = qr.make_image(fill_color='#000000', back_color="#DED6BF")

        # QRを描画
        img.paste(img_qr, (614-img_qr.size[0]//2, 860-img_qr.size[1]//2))   # // -> 整数を返す。/ -> 浮動小数ではエラーになる


        # チケット書き出し
        # img.thumbnail(img_save_size)
        img.save(save_src + "/tanabata_skylatern_festival_2020to2021_ticket_GROUP_" + str(row[0]) + ".png", dpi=(300, 300))


    # 完了通知
    tkinter.messagebox.showinfo(systemName, '完了しました！\n')



main()