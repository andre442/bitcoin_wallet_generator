#btc wallet generator
import ecdsa
import hashlib
import binascii
import base58

#generating private key
ecdsaPrivateKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
#generating public key
ecdsaPublicKey = '04' + ecdsaPrivateKey.get_verifying_key().to_string().hex()
hash256FromECDSAPublicKey = hashlib.sha256(binascii.unhexlify(ecdsaPublicKey)).hexdigest()
ridemp160FromHash256 = hashlib.new('ripemd160', binascii.unhexlify(hash256FromECDSAPublicKey))
prependNetworkByte = '00' + ridemp160FromHash256.hexdigest()
hash = prependNetworkByte
for x in range(1,3):
    hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
cheksum = hash[:8]
appendChecksum = prependNetworkByte + cheksum
bitcoinAddress = base58.b58encode(binascii.unhexlify(appendChecksum))

#converting private key FORMAT WIF
private_key_hex = '80' + ecdsaPrivateKey.to_string().hex()
first_sha256 = hashlib.sha256(binascii.unhexlify(private_key_hex)).hexdigest()
second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
final_key = private_key_hex+second_sha256[:8]
WIF = base58.b58encode(binascii.unhexlify(final_key))

#checking if checksum is valid
base58Decoder = base58.b58decode(bitcoinAddress.decode('utf-8')).hex()
prefixAndHash = base58Decoder[:len(base58Decoder)-8]
checksum = base58Decoder[len(base58Decoder)-8:]
hash = prefixAndHash
for x in range(1,3):
    hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
    #print("Hash#", x, " : ", hash)
if(checksum == hash[:8]):
    print("[TRUE] checksum is valid!")
else:
    print("[FALSE] checksum is not valid!")

#storing final keys
BTC_public_key = bitcoinAddress.decode('utf-8')
BTC_private_key = WIF.decode("utf-8")

#generating .txt file
f= open("BTC_wallet.txt","a")
f.write("Public Key: {} \r".format(BTC_public_key))
f.write("Private Key: {} \r\n".format(BTC_private_key))
f.close()

#generating qr_codes
import qrcode
from PIL import Image
from PIL import ImageDraw, ImageFont
data = BTC_public_key
#img_01 = qrcode.make(data)
qr = qrcode.QRCode(version = 7,
                    box_size = 15,
                    border = 5)
qr.add_data(data)
qr.make(fit = True)
img_01 = qr.make_image(fill_color = 'black',
                    back_color = 'white')
data = BTC_private_key
qr = qrcode.QRCode(version = 7,
                    box_size = 15,
                    border = 5)
qr.add_data(data)
qr.make(fit = True)
img_02 = qr.make_image(fill_color = 'red',
                    back_color = 'white')
img_01_size = img_01.size
img_02_size = img_01.size
new_im = Image.new('RGB', (2*img_01_size[0],1*img_01_size[1]), (250,250,250))
draw = ImageDraw.Draw(new_im)
fonts = ImageFont.truetype("arial.ttf",size=45)
new_im.paste(img_01, (0,0))
new_im.paste(img_02, (img_02_size[0],0))
draw.text((75,5), "PUBLIC KEY", (0,0,0),font=fonts)
draw.text((900,5),"PRIVATE KEY", (0,0,0),font=fonts)
new_im.save("Wallet_QR_{}.png".format(BTC_public_key[ 0 : 5 ]), "PNG")
