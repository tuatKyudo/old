#┌─────────────────────────────────
#│ [ YY-BOARD ]
#│ howto.pl - 2006/11/14
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#│ 
#│ Modified by isso. 2007
#│ http://swanbay-web.hp.infoseek.co.jp/index.html
#└─────────────────────────────────

#-------------------------------------------------
#  留意事項
#-------------------------------------------------
sub howto {
	&header;
	print <<EOM;
<div align="center">
<table width="90%" border="$border" cellspacing="$cellspacing" cellpadding="10" class="thread">
<tr><td bgcolor="$tblcol">
<h3>留意事項</h3>
<ol>
<li>この掲示板は<b>クッキー対応</b>です。1度記事を投稿いただくと、お名前、Ｅメール、参照先、削除キーの情報は2回目以降は自動入力されます。（ただし利用者のブラウザがクッキー対応の場合）
<li>投稿内容には、<b>タグは一切使用できません。</b>
<li>記事を投稿する上での必須入力項目は<b>「お名前」</b>と<b>「メッセージ」</b>です。Ｅメール、参照先、題名、削除キーは任意です。
<li>記事には、<b>半角カナは一切使用しないで下さい。</b>文字化けの原因となります。
<li>記事の投稿時に<b>「削除キー」</b>に任意のパスワード（英数字で8文字以内）を入れておくと、その記事は次回<b>削除キー</b>によって修正及び削除することができます。
<li>記事の保持件数は<b>最大$max件</b>です。それを超えると古い順に自動削除されます。
<li>既存の記事に<b>「返信」</b>をすることができます。各記事の上部にある<b>「返信」</b>ボタンを押すと返信用フォームが現れます。
<li>過去の投稿記事から<b>「キーワード」によって簡易検索ができます。</b>トップメニューの<a href="$bbscgi?mode=find&list=$in{'list'}">「ワード検索」</a>のリンクをクリックすると検索モードとなります。
<li>管理者が著しく不利益と判断する記事や他人を誹謗中傷する記事は予\告なく削除することがあります。
</ol>
<p>
改造版の追加機能\
<ol>
<li>独自の判定基準を元に掲示板スパムを判定し投稿排除をしています。
<li>携帯からの閲覧、投稿、編集ができます。
<li>現行記事を投稿された順に表\示(新着順表\示)することができます。
<li>投稿タイトルをクリックすると関連スレッドをピックアップできます。
</ol>
</td></tr></table>
<p>
<form>
<input type="button" value="掲示板に戻る" onclick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  JavaScript無効
#-------------------------------------------------
sub noscript {
	&header;
	print <<EOM;
<table width="100%" border="$border" cellspacing="$cellspacing" cellpadding="$cellpadding" class="thread">
<tr><th bgcolor="$tCol">
  <font color="$tblcol">JavaScriptを利用したメールアドレス表\示について</font>
</th></tr></table>
<p><div align="center">
スパム(一方的迷惑メール)およびウイルス対策のため、JavaScriptを利用したメールアドレス表\示を採用しています。<br>
お手数をおかけしますが、投稿者のメールアドレスを表\示させるためには、JavaScriptを有効にしてください。<br>
<br>
<form action="$bbscgi" target="_top">
<input type="hidden" name="page" value="$page">
<input type="hidden" name="list" value="$in{'list'}">
<input type="submit" value="掲示板へ戻る">
</form>
</div>
<br><hr>
</body>
</html>
EOM
	exit;
}


1;

