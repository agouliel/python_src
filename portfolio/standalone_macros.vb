https://docs.xlwings.org/en/stable/addin.html#xlwings-addin
xlwings quickstart myproject --standalone
This will add the content of the add-in as a single VBA module.
---------------------------------------------------
Path to the AppleScript file:
/Users/agou/Library/Application Scripts/com.microsoft.Excel/xlwings-0.25.3.applescript

VbaHandler("TestString") # Allows to run the script from Script Editor for testing

on VbaHandler(ParameterString)
	set {PYTHONPATH, PythonInterpreter, PythonCommand, WorkbookName, ApplicationFullName, LOG_FILE} to SplitString(ParameterString, "|")
	set ShellCommand to PythonInterpreter & " -B -u -W ignore -c \"import xlwings.utils;xlwings.utils.prepare_sys_path('" & PYTHONPATH & "');" & ¬
		PythonCommand & " \" \"--wb=" & WorkbookName & "\" \"--from_xl=1\" \"--app=" & ApplicationFullName & "\" > /dev/null 2>\"" & LOG_FILE & "\" & "
	try
		do shell script "source ~/.bash_profile"
		return do shell script "source ~/.bash_profile;" & ShellCommand
	on error errMsg number errNumber
		try
			# Try again without sourcing .bash_profile
			return do shell script ShellCommand
		on error errMsg number errNumber
			return 1
		end try
	end try
end VbaHandler

on SplitString(TheBigString, fieldSeparator)
	# From Ron de Bruin's "Mail from Excel 2016 with Mac Mail example": www.rondebruin.nl
	tell AppleScript
		set oldTID to text item delimiters
		set text item delimiters to fieldSeparator
		set theItems to text items of TheBigString
		set text item delimiters to oldTID
	end tell
	return theItems
end SplitString
---------------------------------------------------

VBAProject(myproject.xlsm) -> Modules -> Module1

Sub SampleCall()

VBAProject(myproject.xlsm) -> Modules -> xlwings

#Const App = "Microsoft Excel" 'Adjust when using outside of Excel

VBAProject(myproject.xlsm) -> Class Modules -> Dictionary

---------------------------------------------------

xlwings(xlwings.xlam) -> Modules -> Config


Option Explicit

xlwings(xlwings.xlam) -> Modules -> Extensions

Function sql(query, ParamArray tables())
---------------------------------------------------

xlwings(xlwings.xlam) -> Modules -> Main

Option Explicit
---------------------------------------------------

xlwings(xlwings.xlam) -> Modules -> RibbonXlwings

Option Explicit

---------------------------------------------------

xlwings(xlwings.xlam) -> Modules -> Utils

Option Explicit

xlwings(xlwings.xlam) -> Class Modules -> Dictionary

''
