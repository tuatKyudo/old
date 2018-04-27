#!/usr/bin/perl

# RSS for YY-BOARD Ver1.0.2
# Copyright (c) 2004-2005 by CGI-Store.JP. All Rights Reserved.
# 種別：フリーウェア
# 開発者：CGI-Store.JP
# 連絡先：webmaster@cgi-store.jp
# サポート：ホームページの掲示板のみ
# ホームページ：http://cgi-store.jp/

# ====================================================================
# 注意事項
# ====================================================================

# このCGIを使用したいかなる損害に対して開発者は一切の責任を負いません。
# RSS for YY-BOARD に関する質問は、CGI-Store.JP にお願いします。
# サポートはホームページの掲示板のみで受け付け、
# 直接メールによるサポートは一切行っていません。

# YY-BOARD v5.xx のログにのみ対応しています。
# YY-BOARD の各種派生バージョンでも、ログ形式が同じならば使用可能です。

# YY-BOARD v5.4 を同梱した物もあります。

# ====================================================================
# 設置方法
# ====================================================================

# yyrss.cgiの設定
# 設定項目を間違いの無いように設定してください。
# yyrss.cgiのパーミッションを755等に変更し実行可能な状態にしてください。
# 最後に、yyrss.cgiへのリンクを、YY-BOARDやホームページ等に挿入します。
# 同梱のYY-BOARDには、yyrss.cgiへのリンクを設置済みです。

# ====================================================================
# 文字コード
# ====================================================================

# PerlのモジュールであるJcode.pmが利用不可能を検出すると、
# 自動でjcode.plを利用しようとします。
# その場合jcode.plをパスを合わせてください。

# ====================================================================
# 改版履歴
# ====================================================================

# [Ver1.0.2] UTF-8に対応しました。
#            RSS出力する表示対象の記事を2種類の方法で設定可能にした。
#            YY-BOARDの設定ファイル「yyini.cgi」の読み込みを止めた。
# [Ver1.0.1] 一般公開。

# ====================================================================
# おまけ
# ====================================================================

# 「sample_icon」フォルダにあるアイコンは、
# 脱力オンラインの管理者のご厚意により、
# CGI-Store.Net が、RSS for YY-BOARD と共に配布するものです。

# 脱力オンライン
# http://park2.wakwak.com/~dol/

# ====================================================================
# 設定項目ここから
# ====================================================================

# Jcode.pm or jcode.pl
BEGIN {
	eval {
		require Jcode;
		$rss_UseJcodeModule = 1;
	};
	if ($@) {
		# Jcode.pmが使用できない時にjcode.plを使用します。
		require './lib/jcode.pl';   # ご利用環境に合うようパスを修正してください。
		$rss_UseJcodeModule = 0;
	}
}

# 出力する文字コード（必須）「utf8」はJcode.pm利用時のみ使用可能です。
$rss_oe = 'sjis';    # sjis or euc or utf8

# このファイルのURL（必須）
$rss_file = 'http://www.tuat.ac.jp/~kyudo/cgi-bin/yybbs/yyrss.cgi';

# 掲示板の簡単な説明（必須）
$rss_setsumei = '弓道部掲示板';

# 表示対象
#  1 -> 一番新しいスレッド内の記事より最大件数だけ表示する。
#  2 -> スレッド順にスレッド開始の記事を最大件数だけ表示する。
$rss_type = 2;

# 出力する最大件数（必須）
$rss_num = 5;

# YY-BOARDのタイトル（必須）
$title = 'BBS';

# YY-BOARDのURL（必須）（絶対パス）
$script = 'http://www.tuat.ac.jp/~kyudo/cgi-bin/yybbs/yybbs.cgi';

# YY-BOARDのログファイル
$logfile = './data/log.cgi';

# ====================================================================
# 設定項目ここまで
# ====================================================================


# HTTPヘッダ
if ($rss_UseJcodeModule == 1) {
	if ($rss_oe eq 'utf8') {
		print 'Content-Type: text/xml; charset="UTF-8"' . "\n";
	} elsif ($rss_oe eq 'euc') {
		print 'Content-Type: text/xml; charset="EUC-JP"' . "\n";
	} else {
		print 'Content-Type: text/xml; charset="Shift_JIS"' . "\n";
	}
} else {
	if ($rss_oe eq 'euc') {
		print 'Content-Type: text/xml; charset="EUC-JP"' . "\n";
	} else {
		print 'Content-Type: text/xml; charset="Shift_JIS"' . "\n";
	}
}
print 'Pragma: no-cache' . "\n";
print 'Cache-Control: no-cache' . "\n";
print "\n";

# XMLヘッダ
if ($rss_UseJcodeModule == 1) {
	if ($rss_oe eq 'utf8') {
		print '<?xml version="1.0" encoding="UTF-8" ?>' . "\n";
	} elsif ($rss_oe eq 'euc') {
		print '<?xml version="1.0" encoding="EUC-JP" ?>' . "\n";
	} else {
		print '<?xml version="1.0" encoding="Shift_JIS" ?>' . "\n";
	}
} else {
	if ($rss_oe eq 'euc') {
		print '<?xml version="1.0" encoding="EUC-JP" ?>' . "\n";
	} else {
		print '<?xml version="1.0" encoding="Shift_JIS" ?>' . "\n";
	}
}
print '<rdf:RDF' . "\n";
print '  xmlns="http://purl.org/rss/1.0/"' . "\n";
print '  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"' . "\n";
print '  xmlns:dc="http://purl.org/dc/elements/1.1/"' . "\n";
print '  xml:lang="ja">' . "\n";

# 設定値の文字コードを変換
if ($rss_UseJcodeModule == 1) {
	if ($rss_oe eq 'utf8') {
		Jcode::convert(\$title, 'utf8', 'sjis');
		Jcode::convert(\$script, 'utf8', 'sjis');
		Jcode::convert(\$rss_file, 'utf8', 'sjis');
		Jcode::convert(\$rss_setsumei, 'utf8', 'sjis');
	} elsif ($rss_oe eq 'euc') {
		Jcode::convert(\$title, 'euc', 'sjis');
		Jcode::convert(\$script, 'euc', 'sjis');
		Jcode::convert(\$rss_file, 'euc', 'sjis');
		Jcode::convert(\$rss_setsumei, 'euc', 'sjis');
	}
}
else {
	if ($rss_oe eq 'euc') {
		&jcode::convert(\$title, 'euc', 'sjis');
		&jcode::convert(\$script, 'euc', 'sjis');
		&jcode::convert(\$rss_file, 'euc', 'sjis');
		&jcode::convert(\$rss_setsumei, 'euc', 'sjis');
	}
}

# データ抽出
@viewdata = ();
open(LOGF, $logfile);
flock(LOGF, 2);
$temp = <LOGF>;
$Scheck = 0;
while ($temp = <LOGF>) {
	if ($rss_type == 1) {
		if ((split(/<>/, $temp))[1] eq '') { $Scheck++; }
		if ($Scheck >= 2) { last; }
	} else {
		if ((split(/<>/, $temp))[1] ne '') { next; }
	}
	if ($rss_UseJcodeModule == 1) {
		if ($rss_oe eq 'utf8') {
			Jcode::convert(\$temp, 'utf8', 'sjis');
		} elsif ($rss_oe eq 'euc') {
			Jcode::convert(\$temp, 'euc', 'sjis');
		}
	} else {
		if ($rss_oe eq 'euc') {
			&jcode::convert(\$temp, 'euc', 'sjis');
		}
	}
	push @viewdata, $temp;
}
close(LOGF);

if ($rss_type == 1) {
	@viewdata = reverse @viewdata;
}

if ($rss_num > $#viewdata + 1) { $rss_num = $#viewdata + 1; }

print ' <channel rdf:about="' . $rss_file . '">' . "\n";
print '  <title>' . $title . '</title>' . "\n";
print '  <link>' . $script . '</link>' . "\n";
print '  <description>' . $rss_setsumei . '</description>' . "\n";
print '  <items>' . "\n";
print '   <rdf:Seq>' . "\n";
for ($i = 1; $i <= $rss_num; $i++) {
	print '    <rdf:li rdf:resource="' . $script . '"/>' . "\n";
}
print '   </rdf:Seq>' . "\n";
print '  </items>' . "\n";
print ' </channel>' . "\n";

for ($i = 0; $i <= $#viewdata; $i++) {
	if ($i >= $rss_num) { last; }
	@values = split(/<>/, $viewdata[$i]);
	for ($j = 0; $j <= $#values; $j++) {
		if ($j == 2) {
			$values[$j] = substr($values[$j], 0, 4) . '-' . substr($values[$j], 5, 2) . '-' . substr($values[$j], 8, 2) . 'T' . substr($values[$j], -5, 2) . ':' . substr($values[$j], -2, 2) . '+09:00';
			
		}
		else {
			$values[$j] =~ s/<BR>/ /g;
			$values[$j] =~ s/<br>/ /g;
		}
	}
	print ' <item rdf:about="' . $script . '">' . "\n";
	print '  <title>' . $values[5] . '</title>' . "\n";
	print '  <link>' . $script . '</link>' . "\n";
	print '  <description>' . $values[6] . '</description>' . "\n";
	print '  <dc:date>' . $values[2] . '</dc:date>' . "\n";
	print '  <dc:creator>' . $values[3] . '</dc:creator>' . "\n";
	print ' </item>' . "\n";
}

print '</rdf:RDF>' . "\n";

exit;

