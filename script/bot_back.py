#!/usr/bin/python
# coding: UTF-8
#####################################################
# るしぼっと4
#   Class   ：botメイン処理 (Background)
#   Site URL：https://mynoghra.jp/
#   Update  ：2019/4/8
#####################################################
# Private Function:
#   (none)
#
# Instance Function:
#   (none)
#
# Class Function(static):
#   sRun(cls):
#
#####################################################

from osif import CLS_OSIF
from toot import CLS_Toot
from config import CLS_Config
from regist import CLS_Regist
from userdata import CLS_UserData

from crontest import CLS_CronTest
from botctrl import CLS_BotCtrl
from lookltl import CLS_LookLTL
from lookrip import CLS_LookRIP
from circletoot import CLS_CircleToot
from mylog import CLS_Mylog
from traffic import CLS_Traffic
from usercorr import CLS_UserCorr
from wordcorr import CLS_WordCorr
from gval import gVal
#####################################################
class CLS_BOT_Back() :
#####################################################
	CHR_Account   = ""		#実行アカウント
	CHR_User_path = ""		#ユーザフォルダパス
	
	#使用クラス実体化
	OBJ_Mylog    = ""
	OBJ_Mastodon = ""
	OBJ_MyDon    = ""		# CHR_Account用のmastodonオブジェクト
	OBJ_Traffic  = ""
	OBJ_UserCorr = ""
	OBJ_WordCorr = ""

#####################################################
# 実行
#####################################################
	@classmethod
	def sRun(cls):
		#############################
		# cronテストとconfigのロード
		#   テスト項目
		#     1.データフォルダチェック
		#     2.Master環境情報ロード(チェック)
		#     3.testログ
		#     ※Account、Kindのテストは関数コール時に実施している
		wCLS_Test = CLS_CronTest()
		wRes = wCLS_Test.Run()
		if wRes['Result']!=True :
			return	#問題あり
		
	#############################
	# 初期化
	#############################
		#############################
		# 初期化
		gVal.FLG_Console_Mode = False	#コンソールOFF
		cls.CHR_Account   = wRes['Responce']['Account']
		cls.CHR_User_path = wRes['Responce']['User_path']
		
		cls.OBJ_Mylog    = CLS_Mylog( cls.CHR_User_path + gVal.STR_File['UserLog_path'] )
		cls.OBJ_Traffic  = CLS_Traffic( parentObj=cls )
		cls.OBJ_UserCorr = CLS_UserCorr( parentObj=cls )
		cls.OBJ_WordCorr = CLS_WordCorr( parentObj=cls )
		
		#############################
		# 排他開始 (テストOFFの時)
		if gVal.FLG_Test_Mode==False :
			if CLS_BotCtrl.sLock( cls.CHR_User_path )==True :
				if gVal.FLG_Test_Mode==False :
					cls.OBJ_Mylog.Log( 'a', "排他" )
				else :
					cls.OBJ_Mylog.Log( 'a', "排他(Test)", inView=True )
				
				return	#排他中
		
		#############################
		# 開始ログ
		if gVal.FLG_Test_Mode==False :
			cls.OBJ_Mylog.Log( 'b', "開始" )
		else :
			cls.OBJ_Mylog.Log( 'a', "開始(Test)", inView=True )
		
		#############################
		# 1時間監視
		if CLS_BotCtrl.sChk1HourTime( cls.CHR_User_path )!=True :
			wStr = "CLS_BOT_Back: sChk1HourTime failure"
			cls.OBJ_Mylog.Log( 'a', wStr )
			
			CLS_BotCtrl.sUnlock( cls.CHR_User_path )
			return
		
#		#############################
#		# ユーザ情報読み込み
#		if cls.OBJ_UserCorr.GetUserInfo_Min()!=True :
#			wStr = "CLS_BOT_Sub: GetUserInfo_Min failure"
#			cls.OBJ_Mylog.Log( 'a', wStr )
#			
#			CLS_BotCtrl.sUnlock( cls.CHR_User_path )
#			return
		
#		#############################
#		# 単語辞書読み込み
#		if cls.OBJ_WordCorr.GetWorddic()!=True :
#			wStr = "CLS_BOT_Sub: GetWorddic failure"
#			cls.OBJ_Mylog.Log( 'a', wStr )
#			
#			CLS_BotCtrl.sUnlock( cls.CHR_User_path )
#			return
		
#		#############################
#		# 除外ドメイン読み込み
#		if cls.OBJ_UserCorr.GetDomainREM()!=True :
#			wStr = "CLS_BOT_Sub: GetDomainREM failure"
#			cls.OBJ_Mylog.Log( 'a', wStr )
		
#		#############################
#		# 禁止ワード読み込み
#		if cls.OBJ_WordCorr.GetWordREM()!=True :
#			wStr = "CLS_BOT_Sub: GetWordREM failure"
#			cls.OBJ_Mylog.Log( 'a', wStr )
		
#		#############################
#		# mastodonクラス生成
#		cls.OBJ_Mastodon = CLS_Regist()
#		wRes = cls.OBJ_Mastodon.CreateMastodon( cls.CHR_Account )
#		if wRes['Result']!=True :
#			wStr = "CLS_BOT_Sub: Mastodon connect failure: " + wRes['Reason']
#			cls.OBJ_Mylog.Log( 'a', wStr )
#			
#			CLS_BotCtrl.sUnlock( cls.CHR_User_path )
#			return
#		
#		wRes = cls.OBJ_Mastodon.GetMastodon( cls.CHR_Account )
#		if wRes['Result']!=True :
#			wStr = "CLS_BOT_Sub: Mastodon get failer: " + wRes['Reason']
#			cls.OBJ_Mylog.Log( 'a', wStr )
#			
#			CLS_BotCtrl.sUnlock( cls.CHR_User_path )
#			return
#		
#		cls.OBJ_MyDon = wRes['Responce']	#1個だけ取り出す
		
	#############################
	# mastodon処理
	#############################
##		#############################
##		# LTL監視処理
##		wOBJ_LookLTL = CLS_LookLTL( parentObj=cls )
		








		
	#############################
	# 後処理
	#############################
#		#############################
#		# ユーザ情報書き込み
#		if cls.OBJ_UserCorr.SetUserInfo_Min()!=True :
#			wStr = "CLS_BOT_Sub: SetUserInfo_Min failure"
#			cls.OBJ_Mylog.Log( 'a', wStr )
#		
		#############################
#		# 単語辞書書き込み
#		if cls.OBJ_WordCorr.SetWorddic()!=True :
#			wStr = "CLS_BOT_Sub: SetWorddic failure"
#			cls.OBJ_Mylog.Log( 'a', wStr )
		
		#############################
		# 排他解除
		CLS_BotCtrl.sUnlock( cls.CHR_User_path )
		return


