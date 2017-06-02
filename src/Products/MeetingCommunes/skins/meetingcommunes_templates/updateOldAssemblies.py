## Script (Python) "updateOldAssemblies"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath

brains = context.portal_catalog(meta_type='Meeting')

for brain in brains:
    meeting = brain.getObject()
    currentAssembly = ''
    currentExcused = ''
    currentAbsents = ''

    for item in meeting.getItems(uids=meeting.getRawItems(), ordered=True):

        # Presents
        if item.getItemAssembly() == meeting.getAssembly():
            currentAssembly = ''
        elif item.getItemAssembly(real=True) != currentAssembly:
            currentAssembly = item.getItemAssembly(real=True)

        if item.getItemAssembly(real=True) != currentAssembly:
            item.setItemAssembly(currentAssembly)

        # Excused
        if item.getItemAssemblyExcused() == meeting.getAssemblyExcused():
            currentExcused = ''
        elif item.getItemAssemblyExcused(real=True) != currentExcused:
            currentExcused = item.getItemAssemblyExcused(real=True)

        if item.getItemAssemblyExcused(real=True) != currentExcused:
            item.setItemAssemblyExcused(currentExcused)

        # Absents
        if item.getItemAssemblyAbsents() == meeting.getAssemblyAbsents():
            currentAbsents = ''
        elif item.getItemAssemblyAbsents(real=True) != currentAbsents:
            currentAbsents = item.getItemAssemblyAbsents(real=True)

        if item.getItemAssemblyAbsents(real=True) != currentAbsents:
            item.setItemAssemblyExcused(currentAbsents)
