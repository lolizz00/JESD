Dim Args
Set Args = WScript.Arguments

if (Args.Count < 1) then
  MsgBox "Error generate version file." + vbCrLf + "Usage:" + vbCrLf + "version-gen.vbs <filename> <projectname>"
else
  'iieo?aai eiy auoiaiiai oaeea
  verfilename = Args(0)
  'iieo?aai aaoo/a?aiy
  vYear  = CStr(Year  (Date))
  vMonth = CStr(Month (Date))
  if Len(vMonth) < 2 then
     vMonth = "0"+vMonth
  end if
  vDay    = CStr(Day    (Date))
  if Len(vDay) < 2 then
     vDay = "0"+vDay
  end if
  vHour  = CStr(Hour  (Time))
  if Len(vHour) < 2 then
     vHour = "0"+vHour
  end if
  vMinute = CStr(Minute (Time))
  if Len(vMinute) < 2 then
     vMinute = "0"+vMinute
  end if
  vSecond = CStr(Second (Time))
  if Len(vSecond) < 2 then
     vSecond = "0"+vSecond
  end if
  if (Args.Count < 2) then
    version_full = "version_full  = """+vDay+"."+vMonth+"."+vYear+" "+vHour+":"+vMinute+":"+vSecond+""""
    version_logo = "version_logo  = """+vYear+vMonth+vDay+""""
  else
    projectname = Args(1)
    version_full = "version_full  = """ + projectname + " "+vDay+"."+vMonth+"."+vYear+" "+vHour+":"+vMinute+":"+vSecond+""""
    version_logo = "version_logo  = """ + projectname + " v"+vYear+vMonth+vDay+""""
  end if
  Set FSO = CreateObject("Scripting.FileSystemObject")
  Set FileOutStream = FSO.OpenTextFile(verfilename, 2, true, 0)
  FileOutStream.Write version_full + vbCrLf
  FileOutStream.Write version_logo + vbCrLf
end if