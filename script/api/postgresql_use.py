#!/usr/bin/python
# coding: UTF-8
#####################################################
# public
#   Class   ：ぽすぐれユーズ
#   Site URL：https://mynoghra.jp/
#   Update  ：2019/9/30
#####################################################
# Private Function:
#   __initIniStatus(self):
#   __initQueryStat(self):
#   __loadDBdata( self, inPath ):
#   __checkDBdata(self):
#   __dbConnect(self):
#   __dbClose(self):
#   __runQuerySelect( self, inQuery ):
#   __runQueryCommit( self, inQuery ):
#
# Instance Function:
#   __init__( self, inPath=None ):
#   GetIniStatus(self):
#   GetQueryStat(self):
#   CreateDBdata( self, inDstPath, inSrcPath ):
#   ChgList( self, inData, outList=[] ):
#
# ◇PostgreSQL実制御
#   Connect( self, inPath=None ):
#   Close(self):
#   RunQuery( self, inQuery=None ):
#   RunExist( self, inObjTable=None, inWhere=None ):
#   RunCount( self, inObjTable=None ):
#
# Class Function(static):
#   (none)
#
#####################################################
# 使い方：
#  1.CreateDBdata( inDstPath, inSrcPath )をコールして接続情報をセットする。
#    inDstPath ..接続情報の元フォーマット(text)
#    inDstPath ..接続情報のパス
#
#  ＜接続情報(text)の書式＞
#----------------------
#hostname=
#database=
#username=
#password=
#----------------------
#
#  2.Connect( inPath=None )で接続する。
#    1で作成した inDstPath 接続情報のパス
#  3.RunQuery( inQuery=None )でクエリを実行する。
#    RunExist( inObjTable=None, inWhere=None )はselect exist。
#  4.GetQueryStat(self)でクエリの実行結果と戻り値を取得する。
#  5.終わったらClose()で切断する。
#    updateの場合は、中でcommitもしてる。
#
#####################################################
# 参考：
#   psycopg2
#     https://qiita.com/hoto17296/items/0ca1569d6fa54c7c4732
#
#####################################################
import os
import codecs
import psycopg2
import shutil
from getpass import getpass

#####################################################
class CLS_PostgreSQL_Use():
#####################################################
	PostgreSQL_use = ""						#PostgreSQLモジュール実体
	IniStatus = ""
	##	"Result"   : False
	##	"Reason"   : None
	##	"Responce" : None
	
	QueryStat = ""
	##	"Result"	: False,
	##	"Reason"	: None,
	##	"Responce"	: None,
	##	"Query"		: "None"

	STR_DBdata = {
		"hostname"		:	"",
		"database"		:	"",
		"username"		:	"",
		"password"		:	""
	}

	DEF_MOJI_ENCODE = 'utf-8'				#ファイル文字エンコード

##	STR_QueryStat = ""
##		"Result"		: False,
##		"Cursol"		: None,
##		"Error"			: None


#####################################################
# 初期化状態取得
#####################################################
	def GetIniStatus(self):
		return self.IniStatus	#返すだけ



#####################################################
# 初期化状態取得
#####################################################
	def __initIniStatus(self):
		self.IniStatus = {
			"Result"   : False,
			"Reason"   : "DB closed",
			"Responce" : None
		}
		return



#####################################################
# クエリ状態取得
#####################################################
	def GetQueryStat(self):
		return self.QueryStat	#返すだけ



#####################################################
# クエリ状態取得
#####################################################
	def __initQueryStat(self):
		self.QueryStat = {
			"Result"	: False,
			"Reason"	: None,
			"Responce"	: None,
			"Query"		: "None"
		}
		return



#####################################################
# 初期化
#####################################################
	def __init__( self, inPath=None ):
		self.Connect( inPath )
		return



#####################################################
# dbdataの作成 ※対話型
#####################################################
	def CreateDBdata( self, inDstPath, inSrcPath ):
		#############################
		# DB接続情報ファイルのチェック
		if( os.path.exists( inSrcPath )==False ) :
			##失敗
			wStr = "CLS_PostgreSQL_Use: CreateDBdata: Default DataBase file is not found: " + inSrcPath + '\n'
			print( wStr )
			return False
		
		if( os.path.exists( inDstPath )==False ) :
			##ファイルがなければコピーする
			try:
				shutil.copyfile( inSrcPath, inDstPath )
			except ValueError as err :
				return False
		
		#############################
		# 開始
		wStr = "DataBaseの接続情報の登録をおこないます。（※先ずPostgreSQLのDBは作成されてることが前提となります）" + '\n'
		print( wStr )
		
		#############################
		# host名
		wStr = '\n' + "DataBaseのhost名を入力してください"
		print( wStr )
		wInput = input( "(def:localhost)=> " ).strip()
		if wInput=="" :
			self.STR_DBdata['hostname'] = "localhost"
		else :
			self.STR_DBdata['hostname'] = wInput
		
		#############################
		# database名
		wStr = '\n' + "DataBaseのdatabase名を入力してください"
		print( wStr )
		wInput = input( "=> " ).strip()
		if wInput=="" :
			print( "DataBaseの接続情報の作成がキャンセルされました" )
			return False	#キャンセル
		self.STR_DBdata['database'] = wInput
		
		#############################
		# username名
		wStr = '\n' + "DataBaseのusername名を入力してください"
		print( wStr )
		wInput = input( "=> " ).strip()
		if wInput=="" :
			print( "DataBaseの接続情報の作成がキャンセルされました" )
			return False	#キャンセル
		self.STR_DBdata['username'] = wInput
		
		#############################
		# password
		wStr = '\n' + "DataBaseのpasswordを入力してください"
		print( wStr )
		wInput = getpass( "=> " ).strip()
		if wInput=="" :
			print( "DataBaseの接続情報の作成がキャンセルされました" )
			return False	#キャンセル
		self.STR_DBdata['password'] = wInput
		
		print( '\n' + "DataBaseの接続テスト中......" + '\n' )
		#############################
		# DB接続テスト
		if self.__dbConnect()!=True :
			#失敗
			wStr = "接続失敗: " + self.IniStatus['Reason']
			print( wStr )
			return False	#キャンセル
		
		###いちお切断
		self.Close()
		print( "DataBaseに接続成功しました!!" + '\n' )
		
		print( "DataBaseの接続情報の作成中......" + '\n' )
		#############################
		# 書き込みデータを作成
		wSetLine = []
		wKeylist = self.STR_DBdata.keys()
		for iKey in wKeylist :
			wLine = iKey + "=" + str(self.STR_DBdata[iKey]) + '\n'
			wSetLine.append(wLine)
		
		#############################
		# ファイル上書き書き込み
##		#############################
##		# 存在チェック
##		if os.path.exists( inDstPath )!=True :
##			wStr = "作成失敗: ファイルがありません: " + inPath
##			print( wStr )
##			return False	#失敗
##		
##		#############################
##		# 書き込み
		try:
			wFile = codecs.open( inDstPath, 'w', self.DEF_MOJI_ENCODE )
			wFile.writelines( wSetLine )
			wFile.close()
		except ValueError as err :
			return False
		
		print( "DataBaseの接続情報の作成 成功!!" + '\n' )
		return True



#####################################################
# dbdata存在チェック
#####################################################
##	def __existDBdata( self, inPath ):
##		wRes = os.path.exists( inPath )
##		return wRes



#####################################################
# dbdataのロード
#####################################################
	def __loadDBdata( self, inPath ):
		#############################
		# DBdata 初期化
		self.STR_DBdata['hostname'] = ""
		self.STR_DBdata['database'] = ""
		self.STR_DBdata['username'] = ""
		self.STR_DBdata['password'] = ""
		
		#############################
		# 存在チェック
		wRes = os.path.exists( inPath )
##		wRes = self.__existDBdata( inPath )
		if wRes==False :
##			self.IniStatus['Reason'] = "CLS_PostgreSQL_Use: __loadDBdata: DBfile is not found"
			self.IniStatus['Reason'] = "CLS_PostgreSQL_Use: __loadDBdata: DBfile is not found: " + inPath
			return False
		
		#############################
		# DB接続情報に読み出す
		try:
			for wLine in open( inPath, 'r'):	#ファイルを開く
				wLine = wLine.strip()
				wLine = wLine.split("=")
				if len(wLine)!=2 :
					continue
				self.STR_DBdata[wLine[0]] = wLine[1]
			
		except ValueError as err :
			self.IniStatus['Reason'] = "CLS_PostgreSQL_Use: __loadDBdata: Load DBfile Failed: " + err
			return False
		
		#############################
		# 正常
		return True



#####################################################
# dbdataチェック
#####################################################
	def __checkDBdata(self):
		#############################
		# 状態のチェック
		if self.STR_DBdata['hostname']=="" or \
		   self.STR_DBdata['database']=="" or \
		   self.STR_DBdata['username']=="" or \
		   self.STR_DBdata['password']=="" :
			wMsg = "CLS_PostgreSQL_Use: __checkDBdata: Load DBfile Invalid: "
			wMsg = wMsg + "hostname=" + self.STR_DBdata['hostname'] + " "
			wMsg = wMsg + "database=" + self.STR_DBdata['database'] + " "
			wMsg = wMsg + "username=" + self.STR_DBdata['username'] + " "
			wMsg = wMsg + "password=" + self.STR_DBdata['password']
			self.IniStatus['Reason'] = wMsg
			return False
		
		#############################
		# 正常
		return True



#####################################################
# DB接続
#####################################################
	def __dbConnect(self):
		self.IniStatus['Result'] = False
		
		#############################
		# DB接続
		try:
			self.PostgreSQL_use = psycopg2.connect( host=self.STR_DBdata['hostname'], database=self.STR_DBdata['database'], user=self.STR_DBdata['username'], password=self.STR_DBdata['password'] )
		except ValueError as err :
			self.IniStatus['Reason'] = "CLS_PostgreSQL_Use: __dbConnect: psycopg2 error: " + err
			return False
		
		#############################
		# DB接続完了
		self.IniStatus['Result'] = True
		return True



#####################################################
# DB切断
#####################################################
	def __dbClose(self):
		#############################
		# DB切断
		try:
			self.PostgreSQL_use.close()
		except ValueError as err :
			self.IniStatus['Reason'] = "CLS_PostgreSQL_Use: __dbClose: psycopg2 error: " + err
			return False
		
		self.IniStatus['Reason'] = "DB closed"
		self.IniStatus['Result'] = False
		return True



#####################################################
# 接続
#####################################################
	def Connect( self, inPath=None ):
		#############################
		# 状態初期化
		self.__initIniStatus()
		
		#############################
		# dbdataのロード
		if inPath==None :
			self.IniStatus['Reason'] = "CLS_PostgreSQL_Use: Connect: The path is not specified"
			return False
		
		if self.__loadDBdata( inPath )!=True :
			return False
		
		#############################
		# 状態のチェック
		if self.__checkDBdata()!=True :
			return False
		
		#############################
		# DB接続
		if self.__dbConnect()!=True :
			return False
		
		return True



#####################################################
# 切断
#####################################################
	def Close(self):
		#############################
		# DB切断
		if self.__dbClose()!=True :
			return False
		
		return True



#####################################################
# クエリ実行
#####################################################
###	def RunQuery( self, inCommand=None, inQuery=None ):
	def RunQuery( self, inQuery=None ):
		#############################
		# 状態初期化
		self.__initQueryStat()
		
		#############################
		# 実行前チェック
		if inQuery==None :
			self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: RunQuery: None Query"
			return False
		if self.IniStatus['Result']!=True :
			self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: RunQuery: DB not connect"
			return False
		
		#############################
		# コマンド取得
		wCommand = inQuery.split(" ")
		if len( wCommand )<=1 :
			self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: RunQuery: Query is not correct: " + inQuery
			return False
		wCommand = wCommand[0]
		
		# チェック
		if wCommand!="select" and \
		   wCommand!="create" and \
		   wCommand!="drop"   and \
		   wCommand!="insert" and \
		   wCommand!="delete" and \
		   wCommand!="update" :
			self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: RunQuery: Unknown command: " + inQuery
			return False
		
		#############################
		# クエリ実行
		if wCommand=="select" :
			if self.__runQuerySelect( inQuery )!=True :
				return False
		else :
			if self.__runQueryCommit( inQuery )!=True :
				return False
		
		#############################
		# 正常
		self.QueryStat['Result'] = True
		return True

#############################
###	def __runQuery( self, inQuery, inFLGresp=False, inFLGcommit=False ):
	def __runQuerySelect( self, inQuery ):
		with self.PostgreSQL_use.cursor() as wCur :
			try:
				#############################
				# 本実行
				self.QueryStat['Query'] = inQuery	#デバック用記録
				wCur.execute( inQuery )
				
				#############################
				# 結果を格納
				wColum = []
				for wCol in wCur.description :
					wColum.append( wCol.name )
				self.QueryStat['Responce'] = {
					"Collum" : wColum,
					"Data"   : wCur.fetchall()
				}
			
			except ValueError as err :
				self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: __runQuerySelect: Query error: " + err
				return False
		
		#############################
		# 正常
		return True

#############################
	def __runQueryCommit( self, inQuery ):
		with self.PostgreSQL_use.cursor() as wCur :
			try:
				#############################
				# 本実行
				self.QueryStat['Query'] = inQuery	#デバック用記録
				wCur.execute( inQuery )
				
				#############################
				# commit
				self.PostgreSQL_use.commit()
			
			except ValueError as err :
				self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: __runQueryCommit: Query error: " + err
				return False
		
		#############################
		# 正常
		return True



#####################################################
# クエリ実行  存在チェック
#####################################################
	def RunExist( self, inObjTable=None, inWhere=None ):
		#############################
		# 状態初期化
		self.__initQueryStat()
		
		#############################
		# 実行前チェック
		if inObjTable==None :
			self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: RunExist: None Object table"
			return False
		if inWhere==None :
			self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: RunExist: None Where"
			return False
		if self.IniStatus['Result']!=True :
			self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: RunExist: DB not connect"
			return False
		
		#############################
		# クエリ作成
		wQuery = "select exists (select * from " + \
					inObjTable + " where " + \
					inWhere + ");"
		
		#############################
		# クエリ実行
		with self.PostgreSQL_use.cursor() as wCur :
			try:
				#############################
				# 本実行
				self.QueryStat['Query'] = wQuery	#デバック用記録
				wCur.execute( wQuery )
				
				#############################
				# 結果を格納
				wRes = wCur.fetchall()
				self.QueryStat['Responce'] = wRes[0][0]
			
			except ValueError as err :
				self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: RunExist: Query error: " + err
				return False
		
		#############################
		# 正常
		self.QueryStat['Result'] = True
		return True



#####################################################
# クエリ実行  レコード数
#####################################################
	def RunCount( self, inObjTable=None ):
		#############################
		# 状態初期化
		self.__initQueryStat()
		
		#############################
		# 実行前チェック
		if inObjTable==None :
			self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: RunCount: None Object table"
			return False
		if self.IniStatus['Result']!=True :
			self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: RunCount: DB not connect"
			return False
		
		#############################
		# クエリ作成
		wQuery = "select count(*) from " + \
					inObjTable + \
					";"
		
		#############################
		# クエリ実行
		with self.PostgreSQL_use.cursor() as wCur :
			try:
				#############################
				# 本実行
				self.QueryStat['Query'] = wQuery	#デバック用記録
				wCur.execute( wQuery )
				
				#############################
				# 結果を格納
				wRes = wCur.fetchall()
				self.QueryStat['Responce'] = wRes[0][0]
			
			except ValueError as err :
				self.QueryStat['Reason'] = "CLS_PostgreSQL_Use: RunCount: Query error: " + err
				return False
		
		#############################
		# 正常
		self.QueryStat['Result'] = True
		return True



#####################################################
# クエリ結果をリスト型に取りだす
#   ※共通フル取得
#####################################################
	def ChgList( self, inData, outList=[] ):
		if len( inData )==0 :
			return False
		
		wList = outList
		#############################
		# カウント値の取り出し
		for wLineTap in inData :
			wGetTap = []
			for wCel in wLineTap :
##				wCel = wCel.strip()
				wGetTap.append( wCel )
			wList.append( wGetTap )
		
		return True






## cd /home/starregion/wsgi/strg_run/


##	>>> import psycopg2
##	# コネクション作成
##	>>> conn = psycopg2.connect("dbname=test host=localhost user=postgres")
##	# カーソル作成
##	>>> cur = conn.cursor()
##	# SQLコマンド実行 (今回はテーブル作成)
##	>>> cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
##	# SQLコマンド実行 (プレースホルダー使用。エスケープも勝手にされる)
##	>>> cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
##	# SQL結果を受け取る
##	>>> cur.execute("SELECT * FROM test;")
##	>>> cur.fetchone()
##	(1, 100, "abc'def")
##	# コミット
##	>>> conn.commit()
##	# クローズ
##	>>> cur.close()
##	>>> conn.close()


####カラム名の取得
## select 
##	* 
## from 
## 	information_schema.columns 
## where 
##	table_catalog='データベース名' 
##	and 
##	table_name='テーブル名' 
## order by 
##	ordinal_position;
##







#####################################################
# HTML作成
#####################################################
def create_HTML( user, dbres ):
	
	wStr = '<!DOCTYPE html>'
	wStr = wStr + '<html>'
	wStr = wStr + '<head>'
	wStr = wStr + '<meta charset="utf-8" />'
	wStr = wStr + '<title>TEST</title>'
	wStr = wStr + '</head>'
	wStr = wStr + '<body>'
	wStr = wStr + user + '<br />'
	wStr = wStr + dbres + '<br />'
	wStr = wStr + '</body></html>'
	
	return wStr



