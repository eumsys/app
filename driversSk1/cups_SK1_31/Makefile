CC = gcc
CFLAGS = -Wall -O2 -DMODEL_SK1
LDFLAGS = -lcupsimage -lcups
FILTER_SRC = rastertosanei.c
FILTER_TARGET = rastertosanei
FILTER_INSTALL_PATH = /usr/lib/cups/filter/

PPD_SRC = sanei.drv
PPD_TARGET = ppd/sanei_sk1_31.ppd

RELEASE_DIR = sanei_cups
RELEASE_TARGET = sanei_cups.tar.gz

all: $(PPD_TARGET) $(FILTER_TARGET)

$(FILTER_TARGET): $(FILTER_SRC)
	$(CC) $(CFLAGS) -o $(FILTER_TARGET) $(FILTER_SRC) $(LDFLAGS)

$(PPD_TARGET): $(PPD_SRC)
	ppdc $(PPD_SRC)

clean:
	rm -f $(FILTER_TARGET)
	rm -f $(PPD_TARGET)
	rm -rf ppd
	rm -f $(RELEASE_TARGET)
	rm -rf $(RELEASE_DIR)

install:
	cp -f $(FILTER_TARGET) $(FILTER_INSTALL_PATH)

release:
	if [ ! -e $(RELEASE_DIR) ]; then mkdir $(RELEASE_DIR); fi
	cp -f $(PPD_TARGET) $(RELEASE_DIR)
	cp -f $(FILTER_TARGET) $(RELEASE_DIR)
	tar -czf $(RELEASE_TARGET) $(RELEASE_DIR)
	rm -rf $(RELEASE_DIR)
