execute_process(COMMAND ${PYTHON_EXEC} -m lib2to3 -wn --no-diffs ${FILE} OUTPUT_QUIET ERROR_QUIET)
execute_process(COMMAND ${PYTHON_EXEC} -m lib2to3 -wnd --no-diffs ${FILE} OUTPUT_QUIET ERROR_QUIET)
