import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "../components/MissonCarousel.css";

const MissionCarousel = () => {
  return (
    <section className="mission-carousel">
      <Swiper
        modules={[Navigation, Pagination]}
        navigation
        pagination={{ clickable: true }}
        slidesPerView={3}     
        centeredSlides={true}    
        loop={true}              
        spaceBetween={0}         
        grabCursor={true}
      >




        <SwiperSlide>
          <div className="card">
            <h2>Our Mission in Numbers</h2>
            <div className="impact-stats">
              <div className="stat">
                <h3>500+</h3>
                <p>Volunteers</p>
              </div>
              <div className="stat">
                <h3>120+</h3>
                <p>Events</p>
              </div>
              <div className="stat">
                <h3>10,000+</h3>
                <p>Hours Served</p>
              </div>
            </div>
          </div>
        </SwiperSlide>


        <SwiperSlide>
          <div className="card">
            <h2>Our Mission</h2>
            <p>
              Pine Pals connects volunteers with meaningful opportunities to 
      support communities, protect the environment, and make a lasting impact.
            </p>
          </div>
        </SwiperSlide>


        <SwiperSlide>
          <div className="card">
            <h2>About Us</h2>
            <p>
              Learn more about who we are, our story, and how you can join us
              in making a difference.
            </p>
            <button className="primary-btn">About Us</button>
          </div>
        </SwiperSlide>

        <SwiperSlide>
          <div className="card">
            <h2>FAQs</h2>
            <p>Have questions? We’ve got answers to help you get started.</p>
            <button className="primary-btn">Read FAQs</button>
          </div>
        </SwiperSlide>
      </Swiper>
    </section>
  );
};

export default MissionCarousel;
