# bookings/views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.forms import UserCreationForm
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import  HTTP_200_OK,HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,HTTP_201_CREATED
from .models import Movie, Show, Booking
from .serializers import MovieSerializer, ShowSerializer, BookingSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import razorpay
# bookings/views.py
from django.conf import settings


# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# User Authentication APIs

@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    form = UserCreationForm(data=request.data)
    if form.is_valid():
        form.save()
        return Response("account created successfully", status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Delete the existing authentication token for the user
    Token.objects.filter(user=request.user).delete()

    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes((AllowAny,))
def list_movie(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)



# User APIs

@api_view(['GET'])
@permission_classes([AllowAny,])
def show_list(request, movie_id):
    shows = Show.objects.filter(movie_id=movie_id)
    serializer = ShowSerializer(shows, many=True)
    return Response(serializer.data)









@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)





from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime, time
import uuid

from .models import Show, Booking
from .serializers import BookingSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_show(request, show_id):
    show = get_object_or_404(Show, id=show_id)

    if show.is_disabled:
        return Response({'error': 'This show is disabled.'}, status=status.HTTP_400_BAD_REQUEST)

    # To prevent booking for past shows
    curr_datetime = datetime.now()
    show_datetime = datetime.combine(show.date, show.show_time)
    if curr_datetime > show_datetime:
        return Response({'error': 'Cannot book for past shows.'}, status=status.HTTP_400_BAD_REQUEST)

    booking_id = str(uuid.uuid4())[:8]
    number_of_tickets = request.data.get('number_of_tickets', 1)

    # Save Booking
    booking = Booking.objects.create(
        user=request.user,
        show=show,
        booking_id=booking_id,
        no_of_tickets=number_of_tickets,
        is_confirmed=True
    )

    # Send confirmation email
    subject = 'Movie Ticket Booking Confirmation'
    message = render_to_string('booking_confirmation_email.html', {'booking': booking})
    plain_message = strip_tags(message)
    from_email = 'your_email@example.com'  # Replace with your email
    to_email = [request.user.email]

    send_mail(subject, plain_message, from_email, to_email, html_message=message)

    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def confirmation(request,id):
    booking = Booking.objects.get(id=id)
    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=HTTP_200_OK)


# def get_show_or_404(show_id):
#     return get_object_or_404(Show, pk=show_id)







# views.py
from datetime import datetime
import uuid
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from reportlab.pdfgen import canvas
from .models import Show, Booking
from razorpay import Client
from django.conf import settings  # Import settings
from qrcode import make as make_qr_code
from PIL import Image
import io
from io import BytesIO
import qrcode

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf(request, id):
    booking = get_object_or_404(Booking, id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="booking_{booking.booking_id}.pdf"'

    # Create PDF content using ReportLab
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Your PDF content generation logic here
    p.drawString(100, 800, f"Booking ID: {booking.booking_id}")
    p.drawString(100, 780, f"Movie Name: {booking.show.movie.title}")
    p.drawString(100, 760, f"Show Date: {booking.show.date}")
    p.drawString(100, 740, f"Show Time: {booking.show.show_time.strftime('%H:%M %p')}")
    p.drawString(100, 720, f"Number of Tickets: {booking.no_of_tickets}")

    # Generate QR code based on booking ID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"Booking ID: {booking.booking_id}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_path = f"media/qr_codes/booking_{booking.booking_id}.png"
    img.save(img_path)

    # Draw QR code image in the PDF
    p.drawInlineImage(img_path, 350, 720, width=100, height=100)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)

    return response



























# # bookings/views.py

# from datetime import datetime
# from qrcode import make as make_qr_code
# from PIL import Image
# from io import BytesIO
# from django.shortcuts import get_object_or_404
# from django.http import HttpResponse
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from reportlab.pdfgen import canvas
# from .models import Movie, Booking, Show
# import razorpay
# from django.conf import settings
# from .serializers import BookingSerializer
# from django.core.mail import EmailMessage

# bookings/views.py

# ... (other imports)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def book_show(request, show_id):
#     show = get_show_or_404(show_id)

#     if show.is_disabled:
#         return Response({'error': 'This show is disabled.'}, status=400)

#     existing_booking = Booking.objects.filter(user=request.user, show=show)
#     if existing_booking.exists():
#         return Response({'error': 'You have already booked for this show.'}, status=400)

#     # Assuming you want to prevent booking for past shows
#     current_datetime = datetime.now()
#     show_datetime = datetime.combine(show.date, show.show_time)
#     if current_datetime > show_datetime:
#         return Response({'error': 'Cannot book for past shows.'}, status=400)

#     # You can add additional checks based on your requirements

#     # Initialize Razorpay client
#     razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#     # Create Booking
#     booking_data = {'user': request.user.id, 'show': show.id}
#     booking_serializer = BookingSerializer(data=booking_data)

#     if booking_serializer.is_valid():
#         booking = booking_serializer.save()

#         # Integrate Razorpay payment processing
#         amount_in_paise = max(int(show.ticket_price * 100), 100)  # Ensure the amount is at least 1 INR
#         payment_data = {
#             'amount': amount_in_paise,
#             'currency': 'INR',
#             'receipt': f'booking_{booking.id}',
#             'payment_capture': 1,
#         }
#         payment_response = razorpay_client.order.create(data=payment_data)

#         # Include payment information in the booking response
#         booking.payment_id = payment_response.get('id')
#         booking.payment_status = payment_response.get('status')
#         booking.save()

#         # Generate QR code for payment
#         qr_code_data = f"Payment for Booking #{booking.id}\nAmount: {booking.show.ticket_price}"
#         qr_code = make_qr_code(qr_code_data)
#         qr_code_image = qr_code.get_image()

#         # Save QR code image to BytesIO buffer
#         qr_code_image_buffer = BytesIO()
#         qr_code_image.save(qr_code_image_buffer, format='PNG')
#         qr_code_image_buffer.seek(0)

#         # Send confirmation email
#         movie_id = show.movie.id
#         # send_product_email_api(request, movie_id, booking)  # Call the email sending function

#         # Include QR code image in the payment response
#         return Response({
#             'booking_id': booking.id,
#             'payment_order_id': payment_response.get('id'),
#             'qr_code_image': qr_code_image_buffer.read(),
#         }, status=201)
#     else:
#         return Response({'error': 'Error creating booking.'}, status=500)








# def get_show_or_404(show_id):
#     return get_object_or_404(Show, pk=show_id)






# from datetime import datetime
# from django.core.mail import send_mail
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import Movie, Booking

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def send_product_email_api(request, movie_id, booking):
#     movie = Movie.objects.get(pk=movie_id)
    
#     if booking.show:
#         show_date = booking.show.date.strftime("%Y-%m-%d %H:%M:%S")
#         show_time = booking.show.show_time.strftime("%I:%M %p")
#         subject3 = f"Show Date: {show_date}"
#         subject4 = f"Show Time: {show_time}"
#     else:
#         subject3 = "Show information not available"
#         subject4 = "Show information not available"

#     # Generate QR code for payment
#     qr_code_data = f"Payment for Booking #{booking.id}\nAmount: {booking.show.ticket_price}"
#     # ... (rest of your code)

#     message = f"You are successfully booking for the movie: {movie.title}"  # Add your custom message or leave it blank
#     from_email = "user123@gmail.com"
#     recipient_list = ["your_mailtrap_inbox@mailtrap.io"]

#     # Sending email
#     send_mail(subject3, message, from_email, recipient_list, fail_silently=False)

#     # ...

#     return Response({'detail': 'Email sent successfully'})



































# ...
# from django.core.mail import EmailMessage

# ...

# def send_booking_confirmation_email(booking, show_id):
#     subject = f"Booking Confirmation - Show #{show_id}"
#     message = f"Thank you for booking! Your booking ID is {booking.id}"

#     # Attach QR code image to the email
#     qr_code_data = f"Booking ID: {booking.id}\nShow: {booking.show.title}\nAmount: {booking.show.ticket_price}"
#     qr_code = make_qr_code(qr_code_data)
#     qr_code_image = qr_code.get_image()
#     qr_code_image_buffer = BytesIO()
#     qr_code_image.save(qr_code_image_buffer, format='PNG')
#     qr_code_image_buffer.seek(0)

#     # Set the "from" address
#     from_address = "user123@gmail.com"

#     # Set the "to" address (Mailtrap.io inbox)
#     recipient_list = "your_mailtrap_inbox@mailtrap.io"

#     # Send email with attachment
#     email = EmailMessage(
#         subject,
#         message,
#         from_address,
#         recipient_list,  # Use the "to" address as the recipient list
#         html_message=message,
#     )

#     # Attach the QR code image to the email
#     email.attach(f'qr_code_show_{show_id}.png', qr_code_image_buffer.read(), 'image/png')

#     email.content_subtype = 'html'  # Set the content type to HTML
#     email.send()





    

# ...

    





# from datetime import datetime
# import razorpay
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Show, Booking
# from .serializers import BookingSerializer



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def book_show(request, show_id):
#     show = get_show_or_404(show_id)

#     if show.is_disabled:
#         return Response({'error': 'This show is disabled.'}, status=400)

#     existing_booking = Booking.objects.filter(user=request.user, show=show)
#     if existing_booking.exists():
#         return Response({'error': 'You have already booked for this show.'}, status=400)

#     # Assuming you want to prevent booking for past shows
#     current_datetime = datetime.now()
#     show_datetime = datetime.combine(show.date, show.show_time)
#     if current_datetime > show_datetime:
#         return Response({'error': 'Cannot book for past shows.'}, status=400)

#     # You can add additional checks based on your requirements

#     # Create Booking
#     booking_data = {'user': request.user.id, 'show': show.id}
#     booking_serializer = BookingSerializer(data=booking_data)

#     if booking_serializer.is_valid():
#         booking = booking_serializer.save()

#         # Integrate Razorpay payment processing
#         amount_in_paise = max(int(show.ticket_price * 100), 100)  # Ensure the amount is at least 1 INR
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         payment_data = {
#             'amount': amount_in_paise,
#             'currency': 'INR',
#             'receipt': f'booking_{booking.id}',
#             'payment_capture': 1,
#         }
#         payment_response = client.order.create(data=payment_data)

#         # Include payment information in the booking response
#         booking.payment_id = payment_response.get('id')
#         booking.payment_status = payment_response.get('status')
#         booking.save()

#         # Generate QR code for payment
#         qr_code_data = f"Payment for Booking #{booking.id}\nAmount: {booking.show.ticket_price}"
#         qr_code = make_qr_code(qr_code_data)
#         qr_code_image = qr_code.get_image()

#         # Save QR code image to BytesIO buffer
#         qr_code_image_buffer = BytesIO()
#         qr_code_image.save(qr_code_image_buffer, format='PNG')
#         qr_code_image_buffer.seek(0)

#         # Include QR code image in the payment response
#         return Response({
#             'booking_id': booking.id,
#             'payment_order_id': payment_response.get('id'),
#             'qr_code_image': qr_code_image_buffer.read(),
#         }, status=201)
#     else:
#         return Response({'error': 'Error creating booking.'}, status=500)






# Admin APIs

# from django.contrib.auth import authenticate
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from rest_framework.authtoken.models import Token
# from rest_framework import status




# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def add_movie(request):
#     serializer = MovieSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)







# @api_view(['PUT'])
# @permission_classes([IsAdminUser])
# def edit_movie(request, movie_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
#     serializer = MovieSerializer(movie, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)



# @api_view(['DELETE'])
# @permission_classes([IsAdminUser])
# def delete_movie(request, movie_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
#     movie.delete()
#     return Response(status=204)



# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def add_show(request):
#     serializer = ShowSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)




# @api_view(['PUT'])
# @permission_classes([IsAdminUser])
# def edit_show(request, show_id):
#     show = get_object_or_404(Show, pk=show_id)
#     serializer = ShowSerializer(show, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)




# @api_view(['DELETE'])
# @permission_classes([IsAdminUser])
# def delete_show(request, show_id):
#     show = get_object_or_404(Show, pk=show_id)
#     show.delete()
#     return Response(status=204)




# @api_view(['PUT'])
# @permission_classes([IsAdminUser])
# def disable_show(request, show_id):
#     show = get_object_or_404(Show, pk=show_id)
#     show.is_disabled = True
#     show.save()
#     return Response({'message': 'Show disabled successfully'}, status=200)






# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def book_show(request, show_id):
#     show = get_show_or_404(show_id)

#     if show.is_disabled:
#         return Response({'error': 'This show is disabled.'}, status=400)

#     existing_booking = Booking.objects.filter(user=request.user, show=show)
#     if existing_booking.exists():
#         return Response({'error': 'You have already booked for this show.'}, status=400)

#     # Assuming you want to prevent booking for past shows
#     current_datetime = datetime.now()
#     show_datetime = datetime.combine(show.date, show.show_time)
#     if current_datetime > show_datetime:
#         return Response({'error': 'Cannot book for past shows.'}, status=400)

#     # You can add additional checks based on your requirements

#     # Create Booking
#     booking_data = {'user': request.user.id, 'show': show.id}
#     booking_serializer = BookingSerializer(data=booking_data)

#     if booking_serializer.is_valid():
#         booking = booking_serializer.save()

#         # Integrate Razorpay payment processing
#         amount_in_paise = int(show.ticket_price * 100)  # Convert to paise (1 INR = 100 paise)
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         payment_data = {
#             'amount': amount_in_paise,
#             'currency': 'INR',
#             'receipt': f'booking_{booking.id}',
#             'payment_capture': 1,
#         }
#         payment_response = client.order.create(data=payment_data)

#         # Include payment information in the booking response
#         booking.payment_id = payment_response.get('id')
#         booking.payment_status = payment_response.get('status')
#         booking.save()

#         # Return confirmation data
#         return Response({'booking_id': booking.id, 'payment_order_id': payment_response.get('id')}, status=201)
#     else:
#         return Response({'error': 'Error creating booking.'}, status=500)


















# from datetime import datetime


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def book_show(request, show_id):
#     show = get_show_or_404(show_id)

#     if show.is_disabled:
#         return Response({'error': 'This show is disabled.'}, status=400)

#     existing_booking = Booking.objects.filter(user=request.user, show=show)
#     if existing_booking.exists():
#         return Response({'error': 'You have already booked for this show.'}, status=400)

#     # Assuming you want to prevent booking for past shows
#     current_datetime = datetime.now()
#     show_datetime = datetime.combine(show.date, show.show_time)
#     if current_datetime > show_datetime:
#         return Response({'error': 'Cannot book for past shows.'}, status=400)

#     # You can add additional checks based on your requirements

#     # Create Booking
#     booking_data = {'user': request.user.id, 'show': show.id}
#     booking_serializer = BookingSerializer(data=booking_data)

#     if booking_serializer.is_valid():
#         booking = booking_serializer.save()

#         # Return confirmation data
#         return Response({'booking_id': booking.id}, status=201)
#     else:
#         return Response({'error': 'Error creating booking.'}, status=500)






# # views.py
# import razorpay
# from django.shortcuts import get_object_or_404
# from django.http import HttpResponse
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import Show, Booking
# from .serializers import BookingSerializer
# from django.core.mail import send_mail
# from reportlab.pdfgen import canvas
# from io import BytesIO
# import qrcode

# # Initialize Razorpay client with your key and secret
# razorpay_client = razorpay.Client(auth=("YOUR_KEY", "YOUR_SECRET"))

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def book_show(request, show_id):
#     show = get_object_or_404(Show, pk=show_id)
    
#     # Check if the show is disabled
#     if show.is_disabled:
#         return Response({'error': 'This show is disabled.'}, status=400)
    
#     # Check if the user has already booked for this show
#     existing_booking = Booking.objects.filter(user=request.user, show=show)
#     if existing_booking.exists():
#         return Response({'error': 'You have already booked for this show.'}, status=400)

#     # Perform payment through Razorpay
#     amount = 50000  # Replace with the actual amount
#     currency = 'INR'
#     order_data = {
#         'amount': amount,
#         'currency': currency,
#         'payment_capture': 1  # Auto capture payment
#     }

#     try:
#         order = razorpay_client.order.create(order_data)
#     except razorpay.errors.BadRequestError as e:
#         # Handle Razorpay authentication failure
#         return Response({'error': 'Razorpay authentication failed.'}, status=500)

#     # Create Booking
#     booking_data = {'user': request.user.id, 'show': show.id}
#     booking_serializer = BookingSerializer(data=booking_data)

#     if booking_serializer.is_valid():
#         booking = booking_serializer.save()

#         # Send confirmation email
#         send_mail(request.user, booking)

#         # Return confirmation data
#         return Response({'booking_id': booking.id, 'order_id': order['id']}, status=201)
#     else:
#         return Response({'error': 'Error creating booking.'}, status=500)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def my_bookings(request):
#     bookings = Booking.objects.filter(user=request.user)
#     serializer = BookingSerializer(bookings, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def download_ticket(request, booking_id):
#     booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

#     # Generate QR code and include in PDF
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)

#     # Add content to PDF
#     p.drawString(100, 800, f"Booking ID: {booking.id}")
#     # Add more details as needed

#     # Generate QR code
#     qr_data = f"Show: {booking.show}, User: {booking.user}, Date: {booking.booking_date}"
#     qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
#     qr.add_data(qr_data)
#     qr.make(fit=True)

#     img = qr.make_image(fill_color="black", back_color="white")
#     img_buffer = BytesIO()
#     img.save(img_buffer)
#     p.drawImage(img_buffer, 100, 700)

#     p.showPage()
#     p.save()

#     buffer.seek(0)
    
#     # Create a response with PDF content
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename=booking_{booking.id}.pdf'
#     response.write(buffer.getvalue())

#     return response

