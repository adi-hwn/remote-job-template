def do_job(status, data):
    global status;
    tlimit = data;
    for i in range(tlimit):
        status = i;