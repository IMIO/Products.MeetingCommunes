## Script (Python) "updateOldAssemblies"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=maxDateTime

from DateTime import DateTime


brains = context.portal_catalog(meta_type='Meeting', getDate={'query': DateTime(maxDateTime), 'range': 'max'})

for brain in brains:
    meeting = brain.getObject()
    currentAssembly = ''
    currentExcused = ''
    currentAbsents = ''

    for item in meeting.getItems(uids=meeting.getRawItems(), ordered=True):

        # Presents
        if item.getItemAssembly(real=True) == meeting.getAssembly():
            currentAssembly = ''
        elif item.getItemAssembly(real=True) != currentAssembly:
            currentAssembly = item.getItemAssembly(real=True)

        if item.getItemAssembly(real=True) != currentAssembly:
            item.setItemAssembly(currentAssembly)

        # Excused
        if item.getItemAssemblyExcused(real=True) == meeting.getAssemblyExcused():
            currentExcused = ''
        elif item.getItemAssemblyExcused(real=True) != currentExcused:
            currentExcused = item.getItemAssemblyExcused(real=True)

        if item.getItemAssemblyExcused(real=True) != currentExcused:
            item.setItemAssemblyExcused(currentExcused)

        # Absents
        if item.getItemAssemblyAbsents(real=True) == meeting.getAssemblyAbsents():
            currentAbsents = ''
        elif item.getItemAssemblyAbsents(real=True) != currentAbsents:
            currentAbsents = item.getItemAssemblyAbsents(real=True)

        if item.getItemAssemblyAbsents(real=True) != currentAbsents:
            item.setItemAssemblyAbsents(currentAbsents)
