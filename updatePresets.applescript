use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions
use al : script "Alfred Library"

on run
	set wf to al's newWorkflow()
	--set p to wf's getPath()
	set p to "/Users/kevinfunderburg/Dropbox/Library/Application Support/Alfred/Alfred.alfredpreferences/workflows/user.workflow.9E93C143-BB02-4044-8B40-285D6999042B/"
	set j to p & "Master Preset.json"
	try
		do shell script "rm " & quoted form of j
	end try
	
	tell application "BetterTouchTool" to trigger_action "{\"BTTPredefinedActionType\" : 105}"
	delay 1
	
	tell application "System Events"
		tell process "BetterTouchTool"
			set theButton to button 5 of window 1
			click theButton
			delay 1
			set exportButton to button 4 of pop over 1 of button 5 of window 1
			ignoring application responses
				click exportButton
				delay 1
				keystroke return
				delay 1
			end ignoring
			
			set isEnabled to false
			repeat until isEnabled is true
				set theButton to first button of window 1 whose (name is "Save")
				if (exists of theButton) is true then
					if enabled of theButton is true then
						set isEnabled to true
					end if
				end if
			end repeat
			
			click theButton
		end tell
	end tell
	delay 1.5
	
	do shell script "mv " & quoted form of (p & "Master Preset.bttpreset") & " " & quoted form of j
	
	display notification "Presets updated successfully"
end run
