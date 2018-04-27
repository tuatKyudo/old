#┌─────────────────────────────────
#│ YY-BOARD v6.21
#│ init.cgi - 2007/09/18
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#│ 
#│ 
#│ ――――――――――――――[注意事項]――――――――――――――
#│ 
#│ 本スクリプトについて、KENT WEBサポート掲示板への質問は禁止です。
#│ 利用規定を守らない場合には本改造スクリプトの使用を一切認めません。
#│ 
#│ ――――――――――――――[注意事項]――――――――――――――
#│ 
#│ 
#│ Antispam Version Modified by isso.
#│ http://swanbay-web.hp.infoseek.co.jp/index.html
#└─────────────────────────────────
$ver = 'YY-BOARD v6.21 Rev2.52';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 改変版CGI設置に関するご質問は設置URLを明記のうえ、下記までお願いします。
#│    http://swanbay-web.hp.infoseek.co.jp/index.html
#│    お問い合わせ前に、「このサイトについて」
#│    http://swanbay-web.hp.infoseek.co.jp/about.html
#│    「よくあるご質問」
#│    http://swanbay-web.hp.infoseek.co.jp/faq.html
#│   「お問い合わせに関する注意事項」
#│    http://swanbay-web.hp.infoseek.co.jp/mail.html
#│    に必ず目を通してください。
#│
#│    最新のNGワードデータファイルは下記よりダウンロードしてください。
#│    http://swanbay-web.hp.infoseek.co.jp/spamdata.shtml
#│
#│    掲示板へのリンク方法をJavascript表示する方法は下記を参照下さい。
#│    http://swanbay-web.hp.infoseek.co.jp/cgi-bin/javascript.html
#│
#│    アクセス制限IPアドレスファイル下記よりダウンロードしてください。
#│    通常、このアクセス拒否IPファイルを利用するは必要ありません。
#│    このファイルを利用したことによるいかなる損害に対しても当方は一切の責任を負いません。
#│    http://swanbay-web.hp.infoseek.co.jp/accessdeny.html
#│＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
#│本改造スクリプトに関してはKENT氏に問い合わせしないようお願いします。
#│￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
#│ 3. 添付の home.gif は L.O.V.E の mayuRin さんによる画像です。
#└─────────────────────────────────
#
# 【ファイル構成例】
#
#  public_html (ホームディレクトリ)
#      |
#      +-- yybbs / yybbs.cgi
#            |     regist.cgi
#            |     admin.cgi
#            |     read.cgi
#            |     registkey.cgi
#            |     init.cgi
#            |
#            +-- lib / jcode.pl
#            |         form.pl
#            |         registkey.pl
#            |         list_log_thread.pl
#            |         list_log_tree.pl
#            |         list_log_topic.pl
#            |         check.pl
#            |         howto.pl
#            |         search.pl
#            |         pastlog.pl
#            |         message.pl
#            |         newsort.pl
#            |         pickup.pl
#            |         keitai.pl   ...携帯用
#            |         webmail.pl  ...WebMail用
#            |         mimew.pl    ...WebMail用
#            |
#            +-- data / log.cgi      ...ログファイル
#            |          count.dat    ...カウンターファイル
#            |          pastno.dat   ...過去ログ用
#            |          cmode.dat    ...カラーモードデータファイル
#            |          color.dat    ...カラーデータファイル
#            |          init.dat     ...カラーデータ初期設定ファイル
#            |          spamdata.cgi ...NGワード
#            |          spamlog.cgi  ...拒否ログ
#            |          denyaddress.cgi ...アクセス禁止データファイル
#            |
#            +-- img / home.gif, bear.gif, ...
#            |
#            +-- past / 0001.cgi ...
#            |
#            +-- mailchk / ...WebMail用

#-------------------------------------------------
# ▼設定項目
#-------------------------------------------------

# タイトル名
$title = "BBS";

# タイトル文字色
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
$tCol = "#008080";

# タイトルサイズ
$tSize = '24px';

# 本文文字フォント
$bFace = '"MS UI Gothic", Osaka, "ＭＳ Ｐゴシック"';

# 本文文字サイズ
$bSize = '13px';

# 壁紙を指定する場合（http://から指定）
$backgif = "http://www.tuat.ac.jp/~kyudo/images/yagasuri.gif";

# 背景色を指定
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
$bgcolor = "#e1f0f0";

# 文字色を指定
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
$text = "#000000";

# リンク色を指定
$link  = "#0000ff";	# 未訪問
$vlink = "#800080";	# 訪問済
$alink = "#ff0000";	# 訪問中

# 初期の表示形式
# thread : スレッド表示（ノーマル）
# tree   : ツリー表示
# topic  : トピック表示
$view_type = 'topic';

# 外部ファイル
$jcode  = './lib/jcode.pl';
$formpl = './lib/form.pl';
$regkeypl = './lib/registkey.pl';
$list_log_thread = './lib/list_log_thread.pl';
$list_log_tree   = './lib/list_log_tree.pl';
$list_log_topic  = './lib/list_log_topic.pl';
$checkpl = './lib/check.pl';
$howtopl = './lib/howto.pl';
$searchpl = './lib/search.pl';
$pastlogpl = './lib/pastlog.pl';
$editlogpl = './lib/editlog.pl';
$messagepl = './lib/message.pl';
$newsortpl = './lib/newsort.pl';
$pickuppl = './lib/pickup.pl';

# カウンタファイル
$cntfile = './data/count.dat';

# 本体ファイルURL
$bbscgi = './yybbs.cgi';

# 更新ファイルURL
$registcgi = './regist.cgi';

# 管理ファイル
$admincgi = './admin.cgi';

# 記事表示ファイル
$readcgi = './read.cgi';

# ログファイル
$logfile = './data/log.cgi';

# 戻り先のURL (index.htmlなど)
$homepage = "../../new_top.shtml";

# 最大記事数
$max = 100;

# アイコン画像のあるディレクトリ
# → フルパスなら http:// から記述する
# → 最後は必ず / で閉じない
$imgurl = "./img";

# アイコンを定義
# →　上下は必ずペアにして、スペースで区切る
$ico1 = 'bear.gif cat.gif cow.gif dog.gif fox.gif hituji.gif monkey.gif zou.gif mouse.gif panda.gif pig.gif usagi.gif';
$ico2 = 'くま ねこ うし いぬ きつね ひつじ さる ぞう ねずみ パンダ ぶた うさぎ';

# 管理者専用アイコン機能 (0=no 1=yes)
# (使い方) 記事投稿時に「管理者アイコン」を選択し、削除キーに
#         「管理パスワード」を入力して下さい。
$my_icon = 0;

# 管理者専用アイコンの「ファイル名」を指定
$my_gif  = 'admin.gif';

# アイコンモード (0=no 1=yes)
$iconMode = 0;

# 返信がつくと親記事をトップへ移動 (0=no 1=yes)
$topsort = 1;

# タイトルにGIF画像を使用する時 (http://から記述)
$t_img = "";
$t_w = 150;	# 画像の幅 (ピクセル)
$t_h = 50;	#   〃  高さ (ピクセル)

# ミニカウンタの設置
#  → 0=no 1=テキスト 2=画像
$counter = 1;

# ミニカウンタの桁数
$mini_fig = 6;

# テキストのとき：ミニカウンタの色
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
$cntcol = "#dd0000";

# 画像のとき：画像ディレクトリを指定
#  → 最後は必ず / で閉じない
$gif_path = "./img";
$mini_w = 8;		# 画像の横サイズ
$mini_h = 12;		# 画像の縦サイズ

# メールアドレスの入力必須 (0=no 1=yes)
$in_email = 0;

# 記事 [タイトル] 部の長さ (全角文字換算)
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
$sub_len = 12;

# 記事の [タイトル] 部の色
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
$subcol = "#006600";

# 記事表示部の下地の色
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
$tblcol = "#ffffff";

# 投稿フォーム及びボタンの文字色
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
$formCol1 = "#f7fafd";	# 下地の色
$formCol2 = "#000000";	# 文字の色

# 家アイコン
$home_gif = "home.gif";	# 家アイコンのファイル名
$home_w = 16;		# 画像の横サイズ
$home_h = 20;		#   〃  縦サイズ

# イメージ参照画面の表示形態
#  1 : JavaScriptで表示
#  2 : HTMLで表示
$ImageView = 1;

# イメージ参照画面のサイズ (JavaScriptの場合)
$img_w = 550;	# 横幅
$img_h = 450;	# 高さ

# ページ当たりの記事表示数 (親記事)
# → 上から順に、スレッド表示、ツリー表示、トピック表示、新着順表示
$pglog{'thread'} = 5;
$pglog{'tree'}   = 10;
$pglog{'topic'}  = 10;
$pglog{'new'}    = 10;

# 投稿があるとメール通知する (sendmail必須)
#  0 : 通知しない
#  1 : 通知するが、自分の投稿記事は通知しない。
#  2 : すべて通知する。
$mailing = 0;

# メールアドレス(メール通知する時)
$mailto = 'xxx@xxx.xxx';

# sendmailパス（メール通知する時）
$sendmail = '/usr/lib/sendmail';

# 文字色の設定
#  →　スペースで区切る
$color = '#000000 #800000 #DF0000 #008040 #0000FF #C100C1 #FF80C0 #FF8040 #000080 #808000 #C0C0C0';

# URLの自動リンク (0=no 1=yes)
$autolink = 1;

# タグ広告挿入オプション
#  → <!-- 上部 --> <!-- 下部 --> の代わりに「広告タグ」を挿入
#  → 広告タグ以外に、MIDIタグ や LimeCounter等のタグにも使用可能
$banner1 = '<!-- 上部 -->';	# 掲示板上部に挿入
$banner2 = '<!-- 下部 -->';	# 掲示板下部に挿入

# ホスト取得方法
# 0 : gethostbyaddr関数を使わない
# 1 : gethostbyaddr関数を使う
$gethostbyaddr = 0;

# アクセス制限（半角スペースで区切る、アスタリスク可）
#  → 拒否ホスト名を記述（後方一致）【例】*.anonymizer.com
$deny_host = '';
#  → 拒否IPアドレスを記述（前方一致）【例】210.12.345.*
$deny_addr = '';

# １回当りの最大投稿サイズ (bytes)
$maxData = 51200;

# 記事の更新は method=POST 限定する場合（セキュリティ対策）
#  → 0=no 1=yes
$postonly = 1;

# 他サイトから投稿排除時に指定する場合（セキュリティ対策）
#  → 掲示板のURLをhttp://から書く
$baseUrl = 'http://www.tuat.ac.jp/~kyudo/cgi-bin/yybbs/';

# 投稿制限（セキュリティ対策）
#  0 : しない
#  1 : 同一IPアドレスからの投稿間隔を制限する
#  2 : 全ての投稿間隔を制限する
$regCtl = 1;

# 制限投稿間隔（秒数）
#  → $regCtl での投稿間隔
$wait = 60;

# 投稿後の処理
#  → 掲示板自身のURLを記述しておくと、投稿後リロードします
#  → ブラウザを再読み込みしても二重投稿されない措置。
#  → Locationヘッダの使用可能なサーバのみ
$location = '';

# 禁止ワード
# → 投稿時禁止するワードをコンマで区切る
$no_wd = '';

# 日本語チェック（投稿時日本語が含まれていなければ拒否する）
# 0=No  1=Yes
$jp_wd = 0;

# URL個数チェック
# → 投稿コメント中に含まれるURL個数の最大値
$urlnum = 7;

## --- <以下は「投稿キー」機能（スパム対策）を使用する場合の設定です> --- ##
#
# ----------------------------------------------------------------
# 「投稿キー」を利用してもスパム投稿される例が報告されています。
# 本改造スクリプトは「投稿キー」以外で徹底的なスパム対策済みです。
# スパム対策目的での「投稿キー」利用は一切必要ありません。
#                                            commented by isso
# ----------------------------------------------------------------
#
# 投稿キーの使用（スパム対策）
# → 0=no 1=yes
$regist_key = 1;

# 投稿キー自動入力(JavaScript有効時)
# 0 : 手動入力
# 1 : 自動入力(推奨)
$autokey = 1;

# 投稿キー画像生成ファイル【URLパス】
$registkeycgi = './registkey.cgi';

# 投稿キー暗号用パスワード（英数字で８文字）
$pcp_passwd = '009byy61';

# 投稿キー許容時間（分単位）
#   投稿フォームを表示させてから、実際に送信ボタンが押される
#   までの可能時間を分単位で指定
$pcp_time = 30;

# 投稿キー画像の大きさ（10ポ or 12ポ）
# 10pt → 10
# 12pt → 12
$regkey_pt = 10;

# 投稿キー画像の文字色
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
# → $textと合わせると違和感がない。目立たせる場合は #dd0000 など。
$moji_col = '#dd0000';

# 投稿キー画像の背景色
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
# → $bgcolorと合わせると違和感がない
$back_col = '#e1f0f0';

#---(以下は「過去ログ」機能を使用する場合の設定です)---#
#
# 過去ログ生成 (0=no 1=yes)
$pastkey = 1;

# 過去ログ用NOファイル
$nofile = './data/pastno.dat';

# 過去ログのディレクトリ
#  → フルパスなら / から記述（http://からではない）
#  → 最後は必ず / で閉じない
$pastdir = './past';

# 過去ログ１ファイルの行数
#  → この行数を超えると次ページを自動生成します
$pastmax = 650;

# １ページ当たりの記事表示数 (親記事)
$pastView = 10;

#-------------------------------------------------
#  追加設定項目 by isso
#-------------------------------------------------


#-------------------------------------------------
# 管理者設定
#-------------------------------------------------
#

# 管理者用パスワード (英数字で８文字以内)
$pass = 'junman66';

# 下記の設定は管理者詐称チェックをする場合のみ必要に応じて変更して下さい。
# 管理者詐称チェック機能に関しては、使い方がわかる方のみ使ってください。
# 使い方がわからないという問い合わせにはお答え致しません。
# 
#   0 : 管理者詐称チェックをしない
#   1 : 管理者詐称チェックをする
$adminchk = 1;

# 管理者詐称チェックをする場合には下記も必ず設定してください。
# 
# 一般利用者が使用できない投稿者名(使用を禁止する名前)を指定
# たとえば、$a_nameで指定した管理者の掲示板表示名を記入します
# 管理者詐称チェックにより使用禁止する名前を設定します。
# 「管理」と設定すると「管理」を含む名前を全て禁止できます。
# (例) $AdminName = "管理人,管理者";
$AdminName = "管理,yuuki,Admin";

# 管理者用ユーザーID、管理者表示を設定します。
# 管理者用ユーザーID、管理者用マスタパスワードで書き込みした場合のみ、
# 投稿者名を「管理者の掲示板表示名($a_name)」で掲示板上に表示します。
# 
# (使用例)
# おなまえを「webmaster」、削除キーを「0123」で投稿する→投稿者名は「管理者」と変換されて表示
# おなまえを直接「管理者」や「管理人」と入力して投稿する→「管理者を名乗れません」とエラー表示
# 管理者以外が管理者になりすますことを防げます。
# 
# 管理者用ユーザーID設定
# $AdminNameで指定した名前以外の管理者しか知り得ない適当なものに変更して下さい。
$admin_id = "Shell";

# 管理者名の表示色
# 指定しない場合は通常の選択色になります。
$a_color  = "#000000";

# 管理者の掲示板表示名(実際に掲示板に表示される管理者の名前)
$a_name   = "Seven &quot;the Admin&quot;";

#-------------------------------------------------
# 投稿設定
#-------------------------------------------------
#
# 投稿フォーム表示
# 投稿フォームを掲示板の上部に表示するか
# メニューにリンク表示するかを選択できます。
#  0 : 投稿フォームを非表示(メニューにてリンク)
#  1 : 投稿フォームを表示(通常)
$postform = 1;

# 投稿許可モード設定
# 投稿許可モードにすると全ての投稿を許可制にすることができます。
# 全ての投稿は管理モードから投稿許可されるまで公開されません。
#  0 : 通常投稿モードにする
#  1 : 投稿許可モードにする
$allowmode = 0;

# 投稿制限
# 登録されたアドレスからの投稿は、書き込みされずに拒否ログに記録されます。
# 投稿を公開する場合には管理モードからスパム投稿ログを閲覧し再投稿処理をして下さい。
# 投稿制限ですから閲覧(アクセス)に関しては制限はありません。
# 
# 投稿制限ホスト名を記述
# (後方一致、半角カンマで区切る、アスタリスク可)
# $dhost = '*-osaka.nttpc.ne.jp,*.o-tokyo.nttpc.ne.jp';
$dhost = '';
# 投稿制限IPアドレスを記述
# (前方一致、半角カンマで区切る、アスタリスク可)
# $daddr = '210.12.345.*,203.232.235.*';
$daddr = '';

# 投稿制限時に表示するメッセージ
$denymsg = 'このメッセージは管理者による公開許可待ちです。';

# 引用部色変更
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
# 色指定を行うと、>で引用された部分の色を変更します
# この機能を使用しない場合は何も記述しないで下さい ($refcol = '';)
$refcol = '#808080';

# 引用文字数/投稿文字数の比率
# 引用文が多すぎる投稿を規制します
# 投稿文字数に対する引用文字数の比率がこの数値以上の場合、"引用部分が多すぎます"とエラー表示します。
# 数値が大きいほど引用に関する制限があまくなり投稿しやすくなります。
# 推奨値は 5～8(倍)で、0に設定するとこの機能は無効になります。
$rrate = 6;

# 引用チェックボックス・返信ボタン設定
# 返信ボタンの横に引用チェックボックス表示するかしないかを選択できます。
#  0 : 親記事のみ返信ボタンを表示(オリジナル仕様)
#  1 : 引用チェックボックスと返信ボタンを全て表示
$re_box = 1;

#-------------------------------------------------
# 掲示板表示設定
#-------------------------------------------------
#
# タイトル一覧表示件数
#  0    : 親記事タイトルを一覧表示しない
#  数値 : 設定件数の親記事タイトルを一覧表示する
#
#  (例)   $alltitle = 20;
#  新着20タイトル(親記事)を一覧表示します。
$alltitle = 20;

# タイトル一覧表示リンク先
# タイトル一覧表示のタイトルをクリックしたときに、
# 該当スレッドの親記事か最新記事のいずれにリンクするかを設定できます。
# 0 : 親記事にリンク
# 1 : 最新記事にリンク
$newtitle = 1;

# 新着順表示の表示数
# 新着順表示のときに1ページに表示する記事数を設定します。
$npage = $pglog{'new'};

# 掲示板表示形式の初期設定
#  thread  : スレッド形式
#  tree    : ツリー形式
#  topic   : トピック形式
#  new     : 新着順形式
$list_ini = "topic";

# 同一スレッド内の最大表示コメント数
# コメント数が設定値より多い場合
# 最新の設定件数のみを表示します。
# 0にするとコメントを省略はせず全て表示します。
$thmax = 0;

# 投稿者文字色。
#  0 : 通常テキスト色にする
#  1 : メッセージ文字色と同じにする
$nam_col = 1;

# 記事にNEWマークを付ける時間
#  24 : 投稿から24時間以内の場合にNEWマークを付ける
$new_time = 24;

# NEWマークの表示形態
#  画像を使用可能
#  (例) $newmark = '<img src="./img/new.gif">';
$newmark = '<font color="#ff3300">New!</font>';

# URLリンクのアンダーライン設定
#  0 : アンダーライン非表示
#  1 : アンダーライン表示
$underline = 0;

# email入力時のアンダーライン設定
#  0 : アンダーライン非表示
#  1 : アンダーライン表示
$emline = 1;

# URL自動リンクの省略設定
# URLが長くなり表示が横に広がる場合、
# 設定文字数以上を省略して表示します。
$max_leng = 80;

# 掲示板有効日数
# 掲示板が設定値(日数)以上利用されない場合、
# 掲示板を自動的に閉鎖します。初期設定は180日。
# 0に設定するとこの機能は無効になります。
# 自動的閉鎖した掲示板は管理画面からワンクリックで再開できます。
$clday = 90;

#-------------------------------------------------
# エラーログ設定
#-------------------------------------------------
# 
# エラーログ記録設定
# 同一ホストからのエラーログを記録する時間間隔
# 同一ホストから続けてエラー投稿があっても
# 設定時間内であれば記録しません。(いたずら対策)
# 初期設定は30(秒)で、0に設定するとエラーログを記録しません。
#  0 : エラーログを記録しない
$errtime = 3;

# エラーログ記録設定
# 記録するエラーの種類を設定します。
# 「全てのエラーを記録」に設定しても
# Internal Server Errorは記録されません。
#  0 : メッセージがある場合のみ記録する【推奨】
#  1 : 全てのエラーを記録する
$errdata = 0;

# エラーログ件数設定
# エラーログの記録最大件数、設定最大件数を超えると
# 古いエラーから順に自動削除されます。初期値は100件。
$errlog_max = 100;

# エラーログファイル
$er_log = './data/error.cgi';

#-------------------------------------------------
# カラーモード設定
#-------------------------------------------------
#
# 掲示板表示形式
# 表示モードをYY-BOARDオリジナル形式に戻す場合には管理画面で行って下さい。
# 表示モードを新表示形式設定時には管理画面でカラーモードを選択してください。

# カラーモードデータファイル
$colorfile = './data/cmode.dat';

# カラーデータファイル
$colordata = './data/color.dat';

# カラーデータ初期設定ファイル
$colorinit = './data/init.dat';

# ツリー表示の選択記事背景色
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
$tree_bc = '#ffffa0';

# メッセージ行間隔設定
# 表示モードがYY-BOARDオリジナル形式のときに有効
# 表示モード変更時には管理画面(カラーモード)で設定
$lheight = "1.3em";

#-------------------------------------------------
# 設定変更不要
#-------------------------------------------------
$border = 1;
$cellspacing = 1;
$cellpadding = 5;
$margin_left = "22px";
$tbl_col0 = $tblcol;
$tbl_col1 = $tblcol;
$topmark = "";
$comark  = "";
$margin_right = "0px";
$width = "90%";

# 機種依存文字使用時のエラーメッセージ
$pdcerror = "機種依存文字は文字化けするためご利用になれません。";

# 機種依存文字の強調表示
$pdch = "<b style='color:#FF0000;background-color:#FFFF00'>";
$pdcf = "</b>";

# 掲示板の利用形式が質問受付形式の場合
# 共通の入力フォームを挿入できます。
# 
# (例)
# $inputform = <<TEXT;
# ------------------------------------
# メーカー:
# 型番:
# 年式:
# ------------------------------------
# TEXT
$inputform = <<TEXT;
TEXT

# 表示ヘッダ(掲示板上部タイトル下)の内容設定(タグ利用可能)
$header = <<HEAD;
<!--ここから-->


<!--ここに掲示板最上部に表示する内容を記述します-->


<!--ここまで-->
HEAD

# 表示フッタ(掲示板最下部)の内容設定(タグ利用可能)
$footer = <<FOOT;
<!--ここから-->


<!--ここに掲示板最下部に表示する内容を記述します-->


<!--ここまで-->
FOOT

#-------------------------------------------------
# メールアドレス入力設定
#-------------------------------------------------
#
# WebMail機能を利用すると、投稿者がメールアドレスを公開することなく
# 掲示板訪問者からのメールを受け取ることができます(sendmail必須)。
# 
# WebMailの利用
#  0 : 利用しない
#  1 : 利用する (sendmail必須です)
$webmail = 0;

# 日本語チェック
# メールのメッセージ内に日本語がある場合のみ
# 送信を許可させることができます。
# 0 : 日本語を含まないメールの送信を許可する
# 1 : 日本語を含まないメールの送信は拒否する
$japanese = 1;

# メールアドレスの過去ログでの表示
# メールアドレスを過去ログで表示するかどうかを設定します。
#  0 : 表示しない
#  1 : 表示する
$pastmail = 0;

$usewebmail = "非公開" ;
if ( $webmail ) { $usewebmail = "非公開(WebMail利用)" ; }

if ($in_email) { $mailopt = "公開" } else { $mailopt = "公開または未記入";}

# [ 変更不要 ] WebMailライブラリ
$webmailpl = './lib/webmail.pl';

# [ 変更不要 ] Webmail認証用ディレクトリ
$mailchk = "./mailchk/";

# [ 変更不要 ] Webmail送信ログファイル
$sendmaillog = 'sendmaillog.cgi';

# [ 変更不要 ] MIMEエンコード
$mimewpl = './lib/mimew.pl';

#-------------------------------------------------
# 携帯用設定
#-------------------------------------------------
# 
# 携帯からの閲覧や投稿、管理モードによる削除に対応していますが、
# 全ての携帯での動作を保証しているわけではありません。

# 携帯の戻り先のURL
# 携帯のトップページが通常のブラウザと異なる場合に
# 携帯用のトップページを設定します。
# $khome = "$homepage";に設定するとブラウザと同じになります。
# (設定例) $khome = "http://www.example.com/i/";
$khome = "$homepage";

# 携帯用スクリプト
$kscript = './lib/keitai.pl';

# 携帯のUSER_AGENT
@keitai = ('DoCoMo','KDDI','J-PHONE','Vodafone','DDIPOCKET','ASTEL','PDXGW','UP.Browser','MOT-','SoftBank','Mozilla');
@type = ('i','e','j','v','d','a','h','e','v','s','p');

# 携帯投稿色
$kcolor = "#5000B0";

# 1ページ表示記事数
$keitai_page = 10;

# 親記事の先頭記号
$treehead = "□";

# コメント先頭記号
$cohead = "・";

# スレッド内コメント先頭記号
$thcohead = "└";

# 携帯モードでのURLの自動リンク
# 0 : 自動リンクしない
# 1 : 自動リンクする
# 「自動リンクする」に設定する場合には、
# ワンクリック詐欺サイトなどの
# 不正サイトへの誘導がないかしっかり監視してください。
$k_link = 0;

# 携帯管理モード時の表示
$keitai_mode = "<font color='#ff0000'>■■管理モード■■</font>";

# Vodafone/J-PHONEのMethod=GET設定
# Vodafone/J-PHONEで投稿できない場合には'GET'に設定します
$v_method = 'POST';

$copyright = "- <a href='http://www.kent-web.com/i/'>YY-BOARD</a> -<br>\n".
		"携帯対応 by <a href='http://swanbay-web.hp.infoseek.co.jp/i/'>isso</a>\n";

#-------------------------------------------------
# スパム投稿(宣伝投稿)拒否設定
#-------------------------------------------------
# 通常は設定変更の必用はありません(特に秒数設定)。
# そのままで運用して頂き、拒否できない投稿が多いか
# あるいは誤処理が多い場合にのみ設定を変更して下さい。
# [基本設定] のみの設定でほとんど全てのスパムを排除できます。
# 通常は [拡張オプション] を使用しないで(ゼロに設定して)下さい。

# ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
# [基本設定]  (ゼロにはせず、必ず設定して下さい)
# ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
# フォーム投稿確認用
# 削除すると動作しませんので絶対に削除しないで下さい。(変更は可)
# 半角の英数字およびアンダースコアのみ設定可能、空白や記号は設定不可です。
# 
# 変更する場合は意味不明な文字列にすることをお薦めします。
# (例) $bbscheckmode = 'L4g_Ks16_4Nd9c';
$bbscheckmode = 'YY_BOARD';

# 削除すると動作しませんので絶対に削除しないで下さい。(変更は可)
# 半角の英数字およびアンダースコアのみ設定可能、空白や記号は設定不可です。
# 特に必用がなければ、変更せずに初期設定のまま運用してください。
# 
# 変更する場合は意味不明な文字列かあるいは
# cancel,clear,delete,reject,reset,erase,annul,effase
# などの語句(を含む文字列)にして下さい。
# ただし、下で設定する$postvalueとは違う文字列にしてください。
# (例) $writevalue = 'k9SL0sv_3rk_wq2';
# (例) $writevalue = 'cancel';
$writevalue = 'cancel';

# 削除すると動作しませんので絶対に削除しないで下さい。(変更は可)
# 半角の英数字およびアンダースコアのみ設定可能、空白や記号は設定不可です。
# 特に必用がなければ、変更せずに初期設定のまま運用してください。
# 
# 変更する場合は意味不明な文字列かあるいは
# cancel,clear,delete,reject,reset,erase,annul,effase
# などの語句(を含む文字列)にして下さい。
# ただし、上で設定した$writevalueとは違う文字列にしてください。
# (例) $postvalue = 'x2oMw7fepc_7ge3';
# (例) $postvalue = 'clear';
$postvalue = 'clear';

# 削除すると動作しませんので絶対に削除しないで下さい。(変更は可)
# 半角の英数字およびアンダースコアのみ設定可能、空白や記号は設定不可です。
# 特に必用がなければ、変更せずに初期設定のまま運用してください。
$formcheck = 'formcheck';

# 掲示板アクセスからの経過時間(秒)
# 投稿フォームを使わないプログラム投稿対策です。
# 投稿者が掲示板を開いて投稿完了するまでの最小時間間隔です。
# 通常は数秒程度に設定しておきます。
# 初期設定は5秒で、ゼロにするとこのチェックは行いません。
$mintime = 5;

# 投稿者が掲示板を開いて投稿完了するまでの最長時間間隔です。
# 通常は7200秒(2時間)～90000秒(25時間)程度に設定しておきます。
# 初期設定は18,000秒(5時間)で、ゼロにするとこのチェックは行いません。
$maxtime = 18000;

# プレビュー非表示の最小時間
# アクセスから投稿までの時間間隔が設定秒数以下の場合、
# 投稿内容をプレビュー表示し、クリック後に書き込み処理をします。
# 通常は初期設定のままで問題ありません。
# 拒否されないスパムが多くなるようでしたら長く設定してください。
# 推奨値15～60(秒)、初期設定は 25(秒)。
$previewmin = 25;

# プレビュー非表示の最大時間
# アクセスから投稿までの時間間隔が設定秒数以上の場合、
# 投稿内容をプレビュー表示し、クリック後に書き込み処理をします。
# 通常は初期設定のままで問題ありません。
# 拒否されないスパムが多くなるようでしたら短く設定してください。
# 推奨値1000～10000(秒)、初期設定は5000秒(約80分)。
$previewmax = 5000;

# チェックデータの符号化処理
# 0 : 符号化しない
# 1 : 符号化する(解析対策)
$fcencode = 1;

# ハッシュキーの変換設定
# 0 : ハッシュキー変換しない
# 1 : ハッシュキー変換をする(スパム対策)
$keychange = 1;

# 句読点を定義
# 句読点として認める記号を設定しておきます。
# 日本語チェックでは句読点を含まないと日本語文ではないと判断します。
@period = ("、","，","。","．","？","！");

# ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
# [投稿拒否ログ設定]  (スパム投稿として拒否された書き込みに関する設定です)
# ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
# 掲示板スパムの投稿拒否ログ
# 数ヶ月間はログを記録し、
# 誤処理がなければ「記録しない」にして下さい。
# 
# 0 : 記録しない
# 1 : 全てのスパム投稿を記録する
# 2 : 日本語の投稿のみを記録し、それ以外はCGIエラーを返す
$spamlog = 2;

# 投稿拒否ログファイル
$spamlogfile = './data/spamlog.cgi';

# 投稿拒否ログ1ページあたりの表示数
# 20に設定すると、拒否ログ閲覧の1ページに20件の拒否ログを表示します
$spamlog_page = 20;

# 投稿拒否ログファイル設定
# 投稿拒否ログの記録最大件数、初期値は200件。
$spamlog_max = 200;

# 投稿拒否ログに残すURL許容数
# スパム投稿に、この設定値以上のURLが書き込まれていた場合、
# 拒否ログにはメッセージ本文を省略して記録します。
# 推奨値は20～50、初期値は20。
$maxurl = 20;

# ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
# [オプション設定]  (必用があれば設定変更して下さい)
# ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
# ホスト情報の取得できないIPアドレスからのアクセス制限
# ホスト情報を取得できないIPアドレスからのアクセスを拒否する場合には 1 にします。
# ニフティ、ぷらら、インフォシーク等を利用している場合や、
# 意味が分からない場合にには 0 のままにしておいてください。
#   0 : アクセスを許可する
#   1 : アクセスを拒否する
$da = 0;

# スパムチェック緩和設定
# クッキーデータがある場合(常連投稿者)には
# スパムチェックを緩和し投稿しやすくします。
# 0 : 通常通りスパムチェックをする
# 1 : スパムチェックを緩和する【推奨】
$cookiecheck = 1;

# URL重複書き込み設定
# URL欄に記入したURLと同一URLがメッセージ内に書かれている場合
# スパム投稿と見なし書き込みを拒否します。
# 日本語のアダルト・出会い系・ワンクリック詐欺スパムに
# この傾向が多く見られます。
# 
# 0 : URLの重複書き込みを許可する
# 1 : 新規投稿の場合のみURLの重複書き込みを拒否する【推奨】
# 2 : 返信でもURLの重複書き込みを拒否する
$urlcheck = 1;

# 名前の最大長設定
# 50に設定すると、名前の長さが50バイト(日本語で25文字)以上の場合に投稿を拒否します。
# ゼロにするとこのチェックは行いません。初期設定は50(推奨値30～50)。
$namelen = 50;

# 投稿メッセージの最低文字数
# メッセージの本文が極端に短い投稿を規制できます。たとえば、" 10 "に設定した場合は、
# 半角文字で10文字、全角文字で5文字以下の場合投稿記事を受理せずにエラーメッセージを表示します。
$minmsg = 10;

# 禁止語句(NGワード、URL)登録ファイル
# 書き込み禁止語句を登録するファイルです。
# このファイルに登録された語句、URLを本文やURL欄に書き込むと投稿拒否されます。
# このファイルを削除すると、禁止語句のチェックは行いません。
$spamdata = './data/spamdata.cgi';

# 正引きスパムチェック用IPアドレスファイル
$spamip = './data/spamip.cgi';

# 最新の禁止語句(NGワード、URL)登録ファイルは下記よりダウンロードしてください。
# http://swanbay-web.hp.infoseek.co.jp/spamdata.shtml

# 禁止語句(NGワード、URL)チェック設定
# 0 : 新規投稿の場合のみ禁止語句(NGワード、URL)チェックをする
# 1 : 返信でも禁止語句(NGワード、URL)チェックをする
$spamdatacheck = 1;

# 0 : メールアドレス欄は禁止語句チェックをしない
# 1 : メールアドレス欄も禁止語句チェックをする
$ngmail  = 1;

# 0 : タイトル欄は禁止語句チェックをしない
# 1 : タイトル欄も禁止語句チェックをする
$ngtitle = 1;

# ここでは、多数のURL書き込みを禁止することができます。
# URLの直接書き込みを許可する場合($comment_url = 0; に設定)は
# URLを書き込める限度数を設定します。
# 10に設定すると、http://～を10以上書き込んだ投稿を拒否します。
# ゼロにするとこのチェックは行いません。初期設定は5(推奨値5～10)。
$spamurlnum = $urlnum;

# 掲示板スパム投稿時の処理
# 0 : CGI(サーバー)エラーを返す
# 1 : すぐに下記のエラーメッセージを表示
# それ以外の数値 : 数値秒後にエラー表示
# 3600に設定すると3600秒(60分)後に下記のエラーメッセージを表示
$spamresult = 1;

# スパムと判断された場合の表示メッセージ
# $spammsg = '投稿は正常に受理されました';
# と設定すると通常の書き込みと投稿拒否を区別できなくすることができます。
# スパム業者に投稿拒否を知られづらくなります。(日本語スパムが多い掲示板向け)
# $spammsg = '';
# とメッセージを設定しない場合にはCGI(サーバー)エラーを返して
# 掲示板が削除されたかのように振る舞います。
# 初期設定は
# $spammsg = '迷惑投稿として正常に処理されました';
$spammsg = '迷惑投稿として正常に処理されました';

# 携帯からのURL入力禁止
# 0 : 携帯からの投稿でもURLの記載を許可する
# 1 : 携帯からの投稿ではURLの記載を禁止する
$keitaiurl = 1;

# チェックデータのJavascript表示化
# 1に設定するとJavascript表示に対応していない
# プログラムからの投稿を排除することができます。
# この機能は携帯に対しては常に無効となります。
# 0 : チェックデータのJavascript表示しない
# 1 : チェックデータのJavascript表示化する(スパム対策)
$javascriptpost = 1;

# 掲示板への直接アクセス投稿制限
# 掲示板へ直接アクセスした場合に投稿を禁止させることができます。
# 掲示板リストを作成して自動投稿をするようなスパムを排除できますが、
# ブックマークから直接掲示板にアクセスした場合やセキュリティソフトを使って
# リファラーを無効に(リンク元情報を削除)している場合も投稿制限を受けます。
# この投稿制限を設定しても携帯からの投稿は制限除外(投稿許可)されます。
# 0 : 投稿を許可する
# 1 : 直接の投稿を禁止する
# 2 : 「Internal Server Error」を返す
$referercheck = 1;

# タイトル入力チェック
# 0 : タイトル未入力のときは「無題」にする
# 1 : タイトル未入力のときはエラー表示する
# 2 : 半角数字のみのタイトルやhttp://を含むタイトルのときはエラー表示する
$suberror = 0;

# メッセージ内の日本語をチェック
# メッセージ内にひらがな、カタカナおよび句読点が含まれているかをチェックします。
# 0 : メッセージに日本語が含まれていなくても投稿を許可する
# 1 : メッセージに日本語が含まれていない場合は投稿を拒否する
$asciicheck = 0;

# メッセージ文字数のチェック設定
# 20に設定すると、URLの記載がある場合に限り
# URL以外の文字数が半角文字で20文字未満、
# 全角文字で10文字未満の場合に投稿を拒否します。
# ゼロにするとこのチェックは行いません。
$characheck = 0;

# 投稿用の合い言葉設定
# 合い言葉の入力を必須とする場合に設定してください。
# (合い言葉設定例)
# $aikotoba = 'ほげほげ';
# 合い言葉を利用しない場合には何も書かないでください。
$aikotoba = '';

# 合い言葉を設定する場合、合い言葉のヒントを書いてください。
# (例) 合い言葉には○○○をひらがなで書いてください
$hint = "合い言葉欄には$aikotobaと書いてください";

# 掲示板を検索サイトロボットの検索対象から外す
# 掲示板を検索サイトロボットの検索対象から外す場合には 1 にします。
#  0 : 検索を許可する
#  1 : 検索対象から外す
$norobot = 1;

# ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
# [拡張オプション設定] (非常用/特に必要性のある場合のみ設定して下さい。)
# ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
# この [拡張オプション] は基本的には設定せず、全てゼロのままご利用下さい。
# この項目を設定しなくてもスパム投稿は排除できます。
# 設定してスパムチェックを厳しくするとスパム投稿は全く無くなりますが、
# それと同時に、投稿時の制限が多いと通常の投稿も減ります。
# 
# 
# [拡張オプション] URLの直接書き込みを禁止する
# URL(http://～)のメッセージ内への直接書き込みを禁止し、
# ttp://～と書き込んだときだけ、URLの書き込みを許可します。
# 0 : URLの直接書き込みを許可する
# 1 : URLの直接書き込みを禁止する(URLを書き込む場合には ttp://～と記述)
$comment_url = 0;

# [拡張オプション] URL転送・短縮URLの掲載禁止設定
# URL転送サービスおよび短縮URLサービスの疑いのあるURLを
# 本文かURL欄に掲載した場合、投稿を禁止させることができます。
# (例) http://symy.jp/ http://xrl.us/ http://jpan.jp/
# http://urlsnip.com/ http://tinyurl.com/ http://204.jp/  など
# 
# 0 : 投稿を許可する
# 1 : 投稿を禁止する
$shorturl = 0;

# [拡張オプション] 不正な削除キーの禁止
# 削除キーに半角スペースを含む場合や、
# 「111111」「aaaaa」のような一字の繰り返しを禁止できます
# 0 : 不正な削除キーを禁止しない
# 1 : 不正な削除キーを禁止する
$ng_pass = 0;

# [拡張オプション] メールアドレスの入力を禁止できます
# 0 : メールアドレスの入力を自由にする
# 1 : メールアドレスの入力を禁止する
# 2 : メールアドレスの入力はアットマークを全角入力「 ＠ 」に限定する
$no_email = 0;
if ($no_email) { $in_email = 0; }

# [拡張オプション] 投稿端末
# 0 : 携帯からの投稿はスパムチェックをゆるめる
# 1 : 携帯からの投稿でも最低限のスパムチェックをする
# 2 : 携帯からの投稿でもブラウザと同様にスパムチェックをする
$keitaicheck = 0;

# [拡張オプション] 投稿IPアドレスチェック設定
# アクセスIPアドレスと投稿IPアドレスが一致しない場合、
# 投稿を拒否することができます。
# 0 : IPアドレスが一致しなくても投稿許可する
# 1 : IPアドレスが一致しない場合は投稿拒否する
$ipcheckmode = 0;

# 投稿許可モード設定
# (設定変更不要)
$postmode = 'スパム投稿';
$alreason = '投稿拒否理由';
if($allowmode) {
	$previewtime = 0;
	$spamresult = 1;
	$spammsg = '正常に処理されました。なお、投稿は管理者の許可後に公開されます。';
	$postmode = '公開許可待ち投稿';
	$alreason = '状態';
}

# ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
# [自動アクセス制限設定] (通常は設定変更の必要はありません) 
# ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
# [自動アクセス制限設定] 制限ファイル
# 掲示板にアクセスしたときにサーバーエラーになる場合には
# 一度このファイルを削除するか、同名で中身が空のファイルを上書き転送してください。
# 通常は変更しないでください。
$denyfile = './data/denyaddress.cgi';

# [自動アクセス制限設定] 制限数設定
# 記録するIPアドレス数を設定します。(初期値50件)
# アクセス制限するIPアドレスが設定数を超える場合は
# 古いデータから順に削除します。
# 通常は変更の必要はありません。
$denynum = 100;

unless (-e $denyfile) {
	if (-e "./denyaddress.cgi") { $denyfile = "./denyaddress.cgi"; }
}

# アクセス制限IPアドレスファイル(外国からのスパム拒否用)
$deny_addr_file = './data/deny_addr_file.cgi';

# アクセス拒否IP追加
@denyaddr= split(/\s+/, $deny_addr);
if (-e $deny_addr_file) {
	open(IN, "$deny_addr_file");
	$deny_addr2 = <IN>;
	close(IN);
	@deny_addr2 = split(/\s+/, $deny_addr2);
	push(@denyaddr, @deny_addr2);
}


#-------------------------------------------------
# ▲設定完了
#-------------------------------------------------

# 記事表示タイプ
%list_type = (
	'thread' => 'スレッド表示',
	'tree'   => 'ツリー表示',
	'topic'  => 'トピック表示',
	'new'    => '新着順表示',
	'pickup'  => '関連記事表示',
	);

#-------------------------------------------------
#  携帯機種チェック
#-------------------------------------------------
sub agent {
	# 携帯機種設定
	my $agent = $ENV{'HTTP_USER_AGENT'};
	$method = 'POST'; $keitai = 'p';

	local ($i) = 0;
	foreach (@keitai) {
		if ($agent =~ /^\Q$_\E/i) { $keitai = $type[$i]; last; }
		$i++;
	}

	#  Vodafone/J-PHONEのMethod
	if ($keitai eq  'v' || $keitai eq  'j') { $method = $v_method; }

	# 携帯モードテスト用
#	$keitai = 'i';

	# 携帯モード
	if (-e "$kscript" && $keitai ne 'p') { require "$kscript"; }
}

#-------------------------------------------------
#  アクセス制限
#-------------------------------------------------
sub axsCheck {
	# IP&ホスト取得
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}

	if ($da) {
		if ($host =~ /\d$/) {
			&error("ホスト名が不明なためアクセスできません。<br>\n".
			"ご利用ネットワークの管理者にDNS登録をお願いしてください。");
		}
	}

	# IPチェック
	local($flg);
	foreach (@denyaddr) {
		s/\./\\\./g;
		s/\*/\.\*/g;

		if ($addr =~ /^$_/i) { $flg = 1; last; }
	}
	if ($flg) {
		&error("アクセスを許可されていません。<br>掲示板管理者までお問い合わせ下さい。");

	# ホストチェック
	} elsif ($host) {

		foreach ( split(/\s+/, $deny_host) ) {
			s/\./\\\./g;
			s/\*/\.\*/g;

			if ($host =~ /$_$/i) { $flg = 1; last; }
		}
		if ($flg) {
			&error("アクセスを許可されていません");
		}
	}
	if ($host eq "") { $host = $addr; }
	if (-e "$denyfile") { &spambot; }
	if ($keitai eq "p") {
		if ($referercheck == 2 && !$ENV{'HTTP_REFERER'}) { &cgi_error; }
	}
}

#-------------------------------------------------
#  フォームデコード
#-------------------------------------------------
sub decode {
	my $buf;
	if ($ENV{'REQUEST_METHOD'} eq "$method") {
		$post_flag=1;
		if ($ENV{'CONTENT_LENGTH'} > $maxData) {
			&error("投稿量が大きすぎます");
		}
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$post_flag=0;
		$buf = $ENV{'QUERY_STRING'};
	}

	undef(%in);
	foreach ( split(/&/, $buf) ) {
		my ($key, $val) = split(/=/);
		$key =~ tr/+/ /;
		$key =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# S-JISコード変換
		&jcode'convert(*val, "sjis", "", "z");

		# エスケープ
		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/\0//g;
		$val =~ s/\r\n/<br>/g;
		$val =~ s/\r/<br>/g;
		$val =~ s/\n/<br>/g;
		$val =~ s/\t//g;

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	$page = $in{'page'};
	$page =~ s/\D//g;
	if ($page < 0) { $page = 0; }
	$mode = $in{'mode'};

	if ($keychange) {
		if ($mode eq "$writevalue" || $mode eq "sendmail") {
			($in{'email'},$in{'url'}) = ($in{'url'},$in{'email'});
			($in{'comment'},$in{'name'}) = ($in{'name'},$in{'comment'});
		}
	}

	# タグ処理
	$in{'name'} =~ s/>/&gt;/g;
	$in{'name'} =~ s/</&lt;/g;
	$in{'name'} =~ s/"/&quot;/g;
	$in{'name'} =~ s/\r//g;
	$in{'name'} =~ s/\n//g;

	$headflag = 0;
}

#-------------------------------------------------
#  エラー処理
#-------------------------------------------------
sub error {
	my ($msg,$spam) = @_;
	# エラーログ
	if (!$spam) {
		if ($errtime) {
			if ($errdata || $in{'comment'}) {
				&write_spamlog("$msg","error");
			}
		}
	}
	&header if (!$headflag);
	print <<EOM;
<div align="center">
<hr width="400"><h3>ERROR !</h3>
<font color="red">$_[0]</font>
<p>
<hr width="400">
<p>
<form>
<input type="button" value="前画面に戻る" onclick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  HTMLヘッダ
#-------------------------------------------------
sub header {
	$headflag=1;

	if ($keitai eq 'p') {
		print "Content-type: text/html\n\n";
		print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="content-script-type" content="text/javascript">
<meta http-equiv="content-style-type" content="text/css">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Expires" content="Mon, 1 Jan 1990 01:01:01 GMT">
<meta http-equiv="Expires" content="0">
EOM
	if ($norobot) {
		print qq|<meta name="ROBOTS" content="NOARCHIVE">\n|;
		print qq|<meta name="ROBOTS" content="NOINDEX,NOFOLLOW">\n|;
	}
	print <<EOM;
<style type="text/css">
<!--
body,td,th { font-size:$bSize; font-family:$bFace; }
EOM
	if ( $scroll ) {
		print qq|body { background-attachment: fixed; }\n|;
	}

	if($underline) {
		print qq|a:hover { color: $alink }\n|;
	} else {
		print qq|a:link    { text-decoration:none; }\n|;
		print qq|a:visited { text-decoration:none; }\n|;
		print qq|a:active  { text-decoration:none; }\n|;
		if($emline) {
			print qq|.e { text-decoration: underline; color:$link; }\n|;
		}
	}
	print qq|a:hover { text-decoration:underline; color:$alink; }\n|;

	print <<EOM;
.n { font-family:Verdana,Helvetica,Arial; }
.b {
	background-color:$formCol1;
	color:$formCol2;
	font-family:Verdana,Helvetica,Arial;
	}
.f {
	background-color:$formCol1;
	color:$formCol2;
	font-size: $bSize;
	}
.topdisp {
	display: none;
}
EOM
	if ($boardmode && -s "$colordata") {
	print <<EOM;
.thread {
	border: $thr_brd solid $tbl_col0;
EOM
	if ($thr_bg && $backgif) {
		print qq|\tbackground-image: url("$backgif")\n|;
	} else {
		print qq|\tbackground-color: $bgcolor;\n|;
	}
	print <<EOM;
	color: $text;
	font-size: $bSize;
	font-family: $bFace
}
.form {
	border: $frm_brd solid $frm_solid;
	background-color: $frm_bc;
	color: $frm_tx;
	font-size: $bSize;
	font-family: $face
}
.alltree {
	border: $allt_brd solid $allt_solid;
	background-color: $allt_col;
	color: $text;
	font-size: $bSize;
	font-family: $bFace
}
input, select {
	border: $btn_brd solid $btn_solid;
	background-color: $formCol1;
	color: $formCol2;
	font-size: 100%;
	font-family: $bFace
}
.menu {
	border: $menu_brd solid $menu_solid;
	background-color: $menu_bg;
	color: $menu_chr;
	font-family: $bFace
	font-size: 100%;
	cursor: hand;
}
.post {
	border: $post_brd solid $post_solid;
	background-color: $post_bg;
	color: $post_chr;
	font-family: $bFace
	font-size: 100%;
	cursor: hand;
}
textarea {
	border-top: $tarea_brd solid $btn_solid;
	border-bottom: $tarea_brd solid $btn_solid;
	border-left: $tarea_brd solid $btn_solid;
	border-right: $tarea_brd solid $btn_solid;
	background-color: $formCol1;
	color: $formCol2;
	font-size: 100%;
}
.radio {
	border: $radio_brd solid $bgcolor;
	background-color: $bgcolor;
	color: $text;
	font-size: 100%;
	font-family: $bFace
}
hr { 
	background-color: $tbl_col0;
	color: $tbl_col0;
	border: none;
	height: 1px;
}
.allow {
	border: $frm_brd solid $frm_solid;
	background-color: $frm_bc;
	color: $text;
	font-family: $face
}
EOM
	}
	print <<EOM;
-->
</style>
EOM
	# JavaScriptヘッダ

	print "<script type=\"text/javascript\">\n",
	"<!-- //\n",
	"function address(){\n",
	"user_name=address.arguments[1];\n",
	"document.write(user_name.link(\"&#109;&#97;&#105;&#108;&#116;&#111;&#58\" + address.arguments[0] + \"&#64;\" + address.arguments[2]));\n",
	"}\n";
	print "function fcheck(){\n",
	"document.write(fcheck.arguments[1] + fcheck.arguments[2] + fcheck.arguments[0] + fcheck.arguments[3]);\n}\n";

	if ($ImageView == 1 && $_[0] eq "ImageUp") {
		print "function ImageUp() {\n";
		print "window.open(\"$bbscgi?mode=image\",\"window1\",\"width=$img_w,height=$img_h,scrollbars=1\");\n}\n";
	}

	print "// -->\n</script>\n";

	print "<title>$title</title></head>\n";
	if ($backgif) {
		print "<body background=\"$backgif\" bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
	} else {
		print "<body bgcolor=\"$bgcolor\" text=\"$text\" link=\"$link\" vlink=\"$vlink\" alink=\"$alink\">\n";
	}

	} else {
		# 携帯用ヘッダ
		print qq|content-type: text/html\n\n|;
		print qq|<html>\n<head>\n|;
		print qq|<meta http-equiv="content-type" content="text/html; charset=shift_jis">\n|;
		print qq|<meta http-equiv="Cache-Control" content="no-cache">\n|;
		print qq|<meta http-equiv="Pragma" content="no-cache">\n|;
		print qq|<title>$title</title>\n</head>\n<body bgcolor="$bgcolor" text="$text">\n|;
	}
}

#-------------------------------------------------
#  自動リンク
#-------------------------------------------------
sub auto_link {
	my ($msg) = @_;
	# ttp置換
	$msg =~ s/([^=^\"]|^)(http:)/$1ttp:/g;
	$msg =~ s/([^=^\"]|^)(ttps?\:[\w\.\~\-\/\?\&\=\+\@\;\#\:\%\,]+)/$1h$2/g;
	# 長いURL対策
	my @url = $msg =~ /([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\+\@\;\#\:\%\,]+)/g;
	my $i = 0;
	my $flg = 0;
	my @part = ();
	my @match = ();
	my @replce = ();
	foreach (@url){
		if ($_ =~ /(https?\:[\w\.\~\-\/\?\&\=\+\@\;\#\:\%\,]+)/) {
			$match[$i] = $&;
			($part[$i],$flg) = &short_link($&);
			if ($flg) {
				($replce[$i] = $part[$i]) =~ s/http/\t/;
				$msg =~ s/([^=^\"]|^)(\Q$match[$i]\E)/$1<a href=\"$match[$i]\" target=\"_blank\">$replce[$i]<\/a>/;
			} else {
				($replce[$i] = $match[$i]) =~ s/http/\t/;
				$msg =~ s/([^=^\"]|^)(\Q$match[$i]\E)/$1<a href=\"$match[$i]\" target=\"_blank\">$replce[$i]<\/a>/;
			}
			$i++;
		}
	}
	$msg =~ s/\t/http/g;
	return $msg;
}

#-------------------------------------------------
#  短縮リンク
#-------------------------------------------------
sub short_link {
	my ($part) = @_;
	my $flg = 0;
	my $match = $part;
	if(length($match) > $max_leng){
		$part = substr($match, 0, abs($max_leng-15));
		$part .= " \.\.\.\.\. ";
		if($match =~ /(.){10}$/) {
			$part .= $&;
		}
		$flg = 1;
	}
	return ($part,$flg);
}

#-------------------------------------------------
#  クッキー発行
#-------------------------------------------------
sub set_cookie {
	local(@cook) = @_;
	local($gmt, $cook, @t, @m, @w);

	@t = gmtime(time + 60*24*60*60);
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# 国際標準時を定義
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# 保存データをURLエンコード
	foreach (@cook) {
		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cook .= "$_<>";
	}

	# 格納
	print "Set-Cookie: YY_BOARD=$cook; expires=$gmt\n";
}

#-------------------------------------------------
#  クッキー取得
#-------------------------------------------------
sub get_cookie {
	local($key, $val, *cook);

	# クッキー取得
	$cook = $ENV{'HTTP_COOKIE'};

	# 該当IDを取り出す
	foreach ( split(/;/, $cook) ) {
		($key, $val) = split(/=/);
		$key =~ s/\s//g;
		$cook{$key} = $val;
	}

	# データをURLデコードして復元
	@cook=();
	foreach ( split(/<>/, $cook{'YY_BOARD'}) ) {
		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("H2", $1)/eg;

		push(@cook,$_);
	}
	return (@cook);
}

#-------------------------------------------------
#  crypt暗号
#-------------------------------------------------
sub encrypt {
	local($inpw) = @_;
	local(@char, $salt, $encrypt);

	@char = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	$salt = $char[int(rand(@char))] . $char[int(rand(@char))];
	$encrypt = crypt($inpw, $salt) || crypt ($inpw, '$1$' . $salt);
	$encrypt;
}

#-------------------------------------------------
#  crypt照合
#-------------------------------------------------
sub decrypt {
	local($in, $dec) = @_;

	local($salt) = $dec =~ /^\$1\$(.*)\$/ && $1 || substr($dec, 0, 2);
	if (crypt($in, $salt) eq $dec || crypt($in, '$1$' . $salt) eq $dec) {
		return (1);
	} else {
		return (0);
	}
}

#-------------------------------------------------
#  時間取得
#-------------------------------------------------
sub get_time {
	$times = shift;
	if (!$times) { $ENV{'TZ'} = "JST-9"; $times = time; }

	my ($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($times);
	my @week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# 日時のフォーマット
	$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",
			$year+1900,$mon+1,$mday,$week[$wday],$hour,$min,$sec);
}

#-------------------------------------------------
#  完了文言
#-------------------------------------------------
sub message {
	local($msg) = @_;

	&header;
	print <<EOM;
<div align="center">
<hr width="400">
<h3>$msg</h3>
<hr width="400">
<p>
EOM
	if($in{'list'} eq "pickup") {
		print qq|<form action="$bbscgi#$in{'num'}">\n|;
	} else {
		print qq|<form action="$bbscgi">\n|;
	}
	print <<EOM;
<input type="hidden" name="list" value="$in{'list'}">
<input type="hidden" name="num" value="$in{'num'}">
<input type="submit" value="掲示板に戻る" class="post">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  カラー設定データ読込
#-------------------------------------------------
sub read_color {
	open(COL,"$colorfile") || &error("カラーモードデータファイル $colorfile がありません。");
	$colormode = <COL>;
	close(COL);

	local $i = 0;
	open(PARA,"$colordata");
	while (<PARA>) {
		($bgcolor,$text,$cntcol,$tCol,$tblcol,$tbl_col0,$thr_brd,$menu_chr,$menu_bg,$menu_solid,$menu_brd,$allt_col,$allt_solid,$allt_brd,$tbl_col1,$tarea_brd,$btn_col,$btx_col,$btn_solid,$btn_brd,$formCol1,$formCol2,$post_chr,$post_bg,$post_solid,$post_brd,$moji_col,$back_col,$radio_brd,$border,$cellspacing,$cellpadding,$topmark,$comark,$margin_left,$margin_right,$subcol,$sub_len,$frm_brd,$frm_bc,$frm_tx,$frm_solid,$refcol,$tree_bc,$scroll,$thr_bg,$lheight,$width) = split(/<>/);
		if (!$width) { $width = "90%"; }
		if ($colormode == $i) { last; }
		$i++;
	}
	close(PARA);
}

#-------------------------------------------------
#  フォームチェックデータ符号化
#-------------------------------------------------
sub encode_bbsmode {
	local($fck) = shift;
	if(!$fck) { $fck = time; }
	if($fcencode) {
		srand;
		local($en) = rand(4); $en++; $en = int($en);
		if ($en%2) { $fck = sprintf("%X", $fck);
		} else { $fck = sprintf("%x", $fck); }
		if ($en == 1)    { $fck =~ tr/[0-9]/[g-p]/; }
		elsif ($en == 2) { $fck =~ tr/[0-9]/[q-z]/; }
		elsif ($en == 3) { $fck =~ tr/[0-9]/[G-P]/; }
		elsif ($en == 4) { $fck =~ tr/[0-9]/[Q-Z]/; }
		$fck = reverse($fck);
	}
	return $fck;
}

#-------------------------------------------------
#  フォームチェックデータ復号
#-------------------------------------------------
sub decode_bbsmode {
	local($fck) = shift;
	$fck2 = $fck;
	if ($fck =~ /[a-z]/i) {
		$fck = reverse($fck);
		$fck =~ tr/[g-p]/[0-9]/;
		$fck =~ tr/[q-z]/[0-9]/;
		$fck =~ tr/[G-P]/[0-9]/;
		$fck =~ tr/[Q-Z]/[0-9]/;
		$fck = sprintf("%d", hex($fck));
	}
	if($fck < 0) { $fck = $fck2; }
	return $fck;
}

#-------------------------------------------------
#  アドレス暗号化
#-------------------------------------------------
sub encode_addr {
	local ($adr,$i);
	$adr = shift;
	if (!$adr) { $adr = $addr; }
	$i = 0;
	foreach (split(/\./, $adr)) {
		$addr[$i] = sprintf("%02x", $_);
		$i++;
	}
	$enadr = substr(crypt(join('',@addr), $addr[0]), 2);
	return $enadr;
}

#-------------------------------------------------
#  エンティティ化
#-------------------------------------------------
sub entity {
	my $str = shift;
	my $ent = "";
	for (0 .. length($str)-1) {
		$ent .= "&#".ord(substr($str, $_, 1)).";";
	}
	return $ent;
}

#-------------------------------------------------
#  エスケープ
#-------------------------------------------------
sub escape {
	my ($str) = @_;
	$str =~ s/[\x00-\x1F\x7F]//g;
	$str =~ s/&/&amp;/g;
	$str =~ s/</&lt;/g;
	$str =~ s/>/&gt;/g;
	$str =~ s/"/&quot;/g;
	$str =~ s/'/&#x27;/g;
	return $str;
}

#-------------------------------------------------
#  スパム/エラーログ記録
#-------------------------------------------------
sub write_spamlog {
	my ($reason,$job) = @_;
	$reason =~ s/\r\n//g;
	$reason =~ s/\r//g;
	$reason =~ s/\n//g;

	if ($job eq "error")  {
		my ($cnam,$ceml,$curl) = &get_cookie;
		if (!$in{'name'})  { $in{'name'}  = $cnam; }
		if (!$in{'email'}) { $in{'email'} = $ceml; }
		if (!$in{'url'})   { $in{'url'}   = $curl; }
		if ($in{'pwd'})    { $ango = &encrypt($in{'pwd'}); }
	}

	my $log_comment = $in{'comment'};
	my $log_name    = $in{'name'};
	my $log_email   = $in{'email'};
	my $log_url     = $in{'url'};
	my $log_sub     = $in{'sub'};
	if (!$log_sub) {
		$log_sub = "無題";
	} 
	if (length($log_comment) < length($log_name)) {
		($log_comment,$log_name) = ($log_name,$log_comment);
	}
	if ($job ne "error")  {
		if($spamlog == 2) {
			# ひらがなを含まないスパムは記録しない
			if ($log_comment !~ /(\x82[\x9F-\xF2])/) {
				if ($spammsg) { &message("$spammsg"); } else { &cgi_error; }
			}
		}
	}

	if ($log_url =~ /\@/ || $log_email && $log_email !~ /\@/) {
		($log_email,$log_url)=($log_url,$log_email);
	}

	my $num = ($log_comment =~ s/http/http/ig);
	if($num >= $maxurl) { $log_comment ="メッセージ内のURL数が$num個と多いため、メッセージ本文削除"; }
	$log_comment =~ s/"/&quot;/g;

	my $times = time;
	my $date = &get_time($times, "log");
	my $log_times = $in{"$bbscheckmode"};
	if (!$log_times) { $log_times = $times; }

	# ログを定義
	my $file = $spamlogfile;
	my $logmax = $spamlog_max;
	if ($job eq "error")  {
		$file = $er_log;
		$logmax = $errlog_max;
	}

	# ログを開く
	open(IN,"+<$file");
	eval { flock(IN, 1); };
	# 古いスパムログを削除
	my $i = 1;
	my $flg = 0;
	my @new = ();
	while (<IN>) {
		# 連続投稿チェック
		if ($i == 1) {
			my ($n,$r,$d,$a,$e,$s,$m,$u,$ho,$p,$c,$ic,$tm) = split(/<>/, $top);
			if (abs(time - $tm) < $errtime) {
				if ($host eq $ho) {
					$flg = 1;
				}
			}
		}
		# 古いスパムログを削除
		if ($i < $logmax) {
			push(@new,$_);
		}
		$i++;
	}
	close(IN);

	# 連続投稿以外を記録
	if (!$flg) {
		# スパム/エラーログを更新
		my $new = "$no<>$in{'reno'}<>$date<>$log_name<>$log_email<>$log_sub<>$log_comment<>$log_url<>$host<>$pwd<>$col[$in{'color'}]<>$in{'icon'}<>$times<>$in{'smail'}<>$reason<>$log_times<>$ENV{'HTTP_REFERER'}<>$ENV{'HTTP_USER_AGENT'}<>$times<>\n";
		unshift (@new,$new);
		open(OUT,"+>$file");
		eval { flock(OUT, 2); };
		seek(OUT, 0, 0);
		print OUT @new;
		close(OUT);
	}
}

#-------------------------------------------------
#  アクセス制限チェック
#-------------------------------------------------
sub spambot {
	my $flag = 0;
	open(IN, "$denyfile");
	eval { flock(IN, 1); };
	while (<IN>) {
		if( $_ =~ /^\s*(\S+)/ ){
			my $part = $1;
			if( $part =~ /\d+\.\d+\.\d+\.\d+/ ){
				if($part && index( $addr, $part ) >= $[ ){
					$flag = 1;
					last;
				}
			}
		}
	}
	close (IN);
	if ($flag) { &cgi_error; }
}

#-------------------------------------------------
#  現在日時取得
#-------------------------------------------------
sub get_date {
	$times = shift;
	if (!$times) { $ENV{'TZ'} = "JST-9"; $times = time; }
	($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($times);
	local(@week) = ('日','月','火','水','木','金','土');

	# 日時のフォーマット
	$date = sprintf("%2d月%2d日(%s) %2d時%2d分",
			$mon+1,$mday,$week[$wday],$hour,$min);
}

#------------------------------------
#  Auto Close
#------------------------------------
sub autoclose {
	print <<EOM;
<div align="left">
<input type="button" value="&lt;&lt; TOP" onclick=window.open("$homepage","_top") class="post">
</div>
<br>
<div align="center">
<h2>掲示板の利用がないため閉鎖中です。管理者までお問い合わせ下さい。</h2>
<p>
<form action="$admincgi" method="post">
<input type="hidden" name="mode" value="admin">
管理PASS: <input type="password" name="pass" size="12">
<input type="submit" value=" 認証 "></form>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  ダミーフォーム
#-------------------------------------------------
sub pseudo {
	if ($keitai eq 'p') {
		print qq|<br>\n<b style|;
		print qq|="font-size:24px; color:#ff0000; background-color:#ffffff; text-align: center;" |;
		print qq|class="topdisp">このフォームからは投稿できません。</b>|;
		print qq|\n<form action="$bbscgi" method="$method" class="topdisp">\n|;
		print qq|<input type="hidden" name="mode" value="wana" class="topdisp">\n|;
		print qq|<table class="topdisp"><tr class="topdisp"><td class="topdisp">name</td>\n|;
		print qq|<td class="topdisp"><input type="text" name="name" size="28" value="" class="topdisp"></td></tr>\n|;
		print qq|<tr class="topdisp"><td class="topdisp">e-mail</td>\n|;
		print qq|<td class="topdisp"><input type="text" name="email" size="28" value="" class="topdisp"></td></tr>\n|;
		print qq|<tr class="topdisp"><td class="topdisp">url</td>\n|;
		print qq|<td class="topdisp">|;
		print qq|<input type="text" name="url" size="36" value="" class="topdisp"></td></tr>\n|;
		print qq|<tr class="topdisp"><td class="topdisp">subject</td>\n|;
		print qq|<td class="topdisp">|;
		print qq|<input type="text" name="subject" size="36" value="" class="topdisp"></td></tr>\n|;
		print qq|<tr class="topdisp"><td class="topdisp">comment</td>\n|;
		print qq|<td class="topdisp">|;
		print qq|<textarea name="comment" cols="56" rows="7" wrap="soft" class="topdisp"></textarea></td></tr>\n|;
		print qq|<tr class="topdisp"><td colspan="2" class="topdisp">\n|;
		print qq|<input type="submit" value="Write" class="topdisp">\n|;
		print qq|<input type="reset" value="Reset" class="topdisp">\n|;
		print qq|</tr></table>\n|;
		print qq|</form>\n\n|;
	}
}



1;


