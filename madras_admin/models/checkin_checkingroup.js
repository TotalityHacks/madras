'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('checkin_checkingroup', {
    'applicant_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'checkin_checkingroup',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

