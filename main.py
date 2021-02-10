print("Checking Imports")
import_list = ['signal', 'psutil', 'time', 'pypresence', 'random']
modules = {}
for package in import_list:
    try:
        modules[package] = __import__(package)
    except ImportError:
        print(f"Package: {package} is missing please install")

print("Loading CONFIG\n")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                              CONFIG
#
#   Change the client_id to your own if you want to use your own assets and name.
#
client_id = '808908940993495040'
#
#   The app can update every 15 seconds according to discord tos (https://discord.com/developers/docs/rich-presence/how-to#updating-presence)
#   However, you can change it to whatever you want at the risk of being Rate-Limited (never have been actualy rate-limited so I dont know the limit. 1 Second works tho)
#
rpc_limit = 5  # int with 1 second being the min
#
#   These are the default quotes or texts displayed. Change to your liking.
#   Button is optional
#
def updateDynamicText():
    cpu_per = round(modules["psutil"].cpu_percent(), 1)
    mem_per = round(modules["psutil"].virtual_memory().percent, 1)
    text = [
        {
            "name": "CPU / RAM",
            "line1": f"CPU: {cpu_per}%",
            "line2": f"RAM: {mem_per}%",
        },
        {
            "name": "The Welcoming",
            "line1": f"Yo we pimp",
            "line2": f"chimping",
            "button": [{"label": "Misfits", "url": "https://scuffed.store/"}, {"label": "Fitz", "url": "https://fitz.fanfiber.com/"}]
        },
    ]
    return {"text": text, "size": len(text)}
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# Spawn Discord RPC connection
RPC = modules["pypresence"].Presence(client_id, pipe=0)
RPC.connect()


# https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
# Thanks to this thread for safe shutdown
class GracefulKiller:
    kill_now = False

    def __init__(self):
        modules["signal"].signal(modules["signal"].SIGINT, self.exit_gracefully)
        modules["signal"].signal(modules["signal"].SIGTERM, self.exit_gracefully)

    def exit_gracefully(self):
        self.kill_now = True


if __name__ == '__main__':
    killer = GracefulKiller()
    print(f"Client ID: {client_id}")
    print(f"Updating every: {rpc_limit} seconds")
    while not killer.kill_now:
        # Presence
        text = updateDynamicText()
        x = modules["random"].randint(0,text["size"]-1)
        try:
            text["text"][x]["button"]
        except KeyError:
            print(RPC.update(details=text["text"][x]["line1"], state=text["text"][x]["line2"]))
        else:
            print(RPC.update(details=text["text"][x]["line1"], state=text["text"][x]["line2"], buttons=text["text"][x]["button"]))

        # https://discord.com/developers/docs/rich-presence/how-to#updating-presence
        # Should only update every 15 seconds, however, this is not a limit and it can go as fast as you want it too.
        # However, you will probabaly get rate-limited and will have to serve a cooldown period if you go too fast.
        modules["time"].sleep(rpc_limit)
    print("I was killed")
    RPC.close()
